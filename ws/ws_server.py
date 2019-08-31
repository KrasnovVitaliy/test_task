import websockets
import asyncio
import logging
import config
import json
import rates.client as rates_client

import ws.handlers as handlers
from ws.response import Response
from db.helpers import DbHelpers
from datetime import datetime
from ws.subscriptions_db import SubscriptionsDB

logger = logging.getLogger(__name__)


class WebsocketServer:
    def __init__(self):
        self.subscriptions_db = SubscriptionsDB()

    def parse_data(self, data):
        if data == "":
            logger.debug("Empty data in request")
            return None

        parsed_data = None
        try:
            parsed_data = json.loads(data)
        except Exception as e:
            logger.error("Could not parse data in request. Error: {}".format(e))

        return parsed_data

    async def handle_request(self, websocket, path):
        try:
            while True:
                data = await websocket.recv()
                logger.debug("Received request data from client: {}".format(data))
                parsed_data = self.parse_data(data)
                if not parsed_data:
                    continue

                logger.debug("Parsed data from client: {}".format(parsed_data))
                rsp = handlers.process_request(parsed_data, websocket)
                logger.debug("Write response to client: {}".format(rsp))
                await websocket.send(rsp)

        except websockets.exceptions.ConnectionClosed:
            logger.debug("Connection closed by client")

    async def send_update_to_clients(self, rates_prices, timestamp):
        """
        Sending rates updates to clients
        :param rates_prices: Rate prices list
        :param timestamp: Rate prise request timestamp
        :return: None
        """

        def create_update_messages_map():
            """
            Creating map of update messages
            :return: Update messages Map<asset_id>rate price
            """
            update_messages = {}
            for rate_price in rates_prices:
                asset_id = DbHelpers().get_assets()[rate_price["Symbol"]]
                update_messages[asset_id] = {"assetName": rate_price["Symbol"], "time": timestamp,
                                             "assetId": asset_id,
                                             "value": DbHelpers().calculate_data(rate_price)}
            return update_messages

        logger.debug("Create update messages map")
        update_messages = create_update_messages_map()
        logger.debug("Get subscribers list")
        subscriptions = self.subscriptions_db.get_subscriptions()

        logger.debug("Sending updates to subscribers")
        for connection in list(subscriptions.keys()):
            try:
                rsp = Response(action="point", message=update_messages[subscriptions[connection]])
                logger.debug("Write update message to client: {}".format(rsp))
                await connection.send(rsp.__str__())

            except websockets.ConnectionClosed:
                logger.debug("Connection has been closed, removing it from subscriptions db")
                self.subscriptions_db.delete_subscription(connection)

    async def ticker_task(self):
        """
        Ticker task to get data from HTTP server process it save to DB and send to subscribed clients
        :return:
        """
        timestamp = int(datetime.utcnow().timestamp())
        logger.info("Tick timestamp: {}".format(timestamp))

        rates_prices = await rates_client.get()
        logger.debug("Received rates prices: {}".format(rates_prices))

        logger.debug("Send rates update to clients")
        await self.send_update_to_clients(rates_prices, timestamp)

        logger.debug("Saving rates prices to DB")
        DbHelpers().save_rates_prices(rates_prices, timestamp)

    async def ticker(self):
        """
        Every second ticker function. Run new coroutine every second.
        :return: None
        """
        while True:
            asyncio.create_task(self.ticker_task())
            await asyncio.sleep(1)

    def run(self):
        """
        Web socket server and every second ticker run function.
        :return: None
        """
        # Loading rates from DB to memory
        logger.info("Loading assets in memory")
        DbHelpers().load_assets()

        logger.info("Starting websocket server on {}:{}".format(config.HOST, config.PORT))
        start_server = websockets.serve(self.handle_request, config.HOST, config.PORT)

        # Creating async tasks
        tasks = [
            asyncio.ensure_future(start_server),
            asyncio.ensure_future(self.ticker())
        ]

        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

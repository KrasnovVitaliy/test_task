from ws.subscriptions_db import SubscriptionsDB
from db.helpers import DbHelpers
import logging
from ws.response import Response

logger = logging.getLogger(__name__)


def subscribe_to_asset(asset_id, connection):
    """
    Subscribe user to asset id
    :param asset_id: Asset id
    :param connection: User WS connection
    :return: response message
    """
    logger.debug("Create subscription to asset id: {}".format(asset_id))
    connection_db = SubscriptionsDB()
    connection_db.set_subscription(connection, asset_id)
    return {"points": DbHelpers().get_init_prices(asset_id)}


def process_request(data, websocket):
    if data['action'] == 'assets':
        rsp = Response(action="assets", message={'assets': DbHelpers().get_assets_list()})
        return rsp.__str__()

    elif data['action'] == 'subscribe':
        rsp = subscribe_to_asset(data['message']['assetId'], websocket)
        return Response(action="asset_history", message=rsp).__str__()
    else:
        return "Unknown action"

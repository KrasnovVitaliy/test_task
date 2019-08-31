import asyncio
import websockets
import json
from websocket import create_connection
import logging

logging.basicConfig(filename=None, filemode='w', level=logging.DEBUG,
                    format='%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)

SERVICE_HOST = "ws://127.0.0.1:8080/"


class TestSimple():
    def test_assets_list(self):
        ws = create_connection(SERVICE_HOST)
        request = {"action": "assets", "message": {}}
        logger.info("Sending asset list request: {}".format(request))
        ws.send(json.dumps(request))
        rsp = ws.recv()
        logger.debug("Received response: {}".format(rsp))
        rsp_data = json.loads(rsp)
        assert rsp_data["action"] == "assets", (
            "Incorrect action value. Expected 'assets' received {}".format(rsp_data["action"]))
        assert len(rsp_data["message"]["assets"]) > 0, "Assets list is empty"
        ws.close()

    def test_subscribe_to_asset(self):
        ws = create_connection(SERVICE_HOST)
        request = {"action": "subscribe", "message": {"assetId": 1}}
        logger.info("Sending subscribe to asset request: {}".format(request))
        ws.send(json.dumps(request))
        rsp = ws.recv()
        logger.debug("Received response: {}".format(rsp))
        rsp_data = json.loads(rsp)
        assert rsp_data["action"] == "asset_history", (
            "Incorrect action value. Expected 'asset_history' received {}".format(rsp_data["action"]))
        assert len(rsp_data["message"]["points"]) > 0, "Assets points list is empty"
        ws.close()

    def test_receive_every_second_update(self):
        ws = create_connection(SERVICE_HOST)
        request = {"action": "subscribe", "message": {"assetId": 1}}
        logger.info("Sending subscribe to asset request: {}".format(request))
        ws.send(json.dumps(request))
        rsp = ws.recv()
        rsp_data = json.loads(rsp)
        assert rsp_data["action"] == "asset_history", (
            "Incorrect action value. Expected 'asset_history' received {}".format(rsp_data["action"]))
        assert len(rsp_data["message"]["points"]) > 0, "Assets points list is empty"

        seconds_assets_updates = []
        for i in range(5):
            rsp = ws.recv()
            seconds_assets_updates.append(json.loads(rsp))
        assert len(seconds_assets_updates) == 5, (
            "Incorrect assets update count, expected receive 5 assets update records, received: {} records".format(
                seconds_assets_updates))

        logger.debug("Checking one record from every second assets update list")
        assert seconds_assets_updates[0]["action"] == "point", (
            "Incorrect action value. Expected 'point' received {}".format(seconds_assets_updates[0]["action"]))

        for field in ["assetName", "time", "assetId", "value"]:
            assert field in seconds_assets_updates[0]["message"], (
                "Field {} does not exist in asset update record".format(field))

        assert (
                seconds_assets_updates[1]["message"]["time"] - seconds_assets_updates[0]["message"]["time"] == 1), (
            "Time diff between to assets updates must be 1 sec. Current diff {}".format(
                seconds_assets_updates[1]["message"]["time"] - seconds_assets_updates[0]["message"]["time"]
            )
        )
        ws.close()

import asyncio
import websockets
import json


# async def hello():
#     uri = "ws://localhost:8080"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             name = input("What's your name? ")
#
#             await websocket.send(name)
#             print(f"> {name}")
#
#             greeting = await websocket.recv()
#             print(f"< {greeting}")
#
# asyncio.get_event_loop().run_until_complete(hello())


# async def send():
#     uri = "ws://localhost:8080"
#     async with websockets.connect(uri) as websocket:
#         request = {"action": "assets", "message": {}}
#
#         await websocket.send(json.dumps(request))
#
#         greeting = await websocket.recv()
#         print(f"< {greeting}")

async def send():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        request = {"action": "subscribe", "message": {"assetId": 1}}

        await websocket.send(json.dumps(request))

        while True:
            greeting = await websocket.recv()
            print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(send())

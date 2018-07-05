# -*- coding: utf-8 -*-
import asyncio
import websockets
import json


class PyAlmondPlus:

    def __init__(self, api_url, loop=asyncio.get_event_loop(), event_callback=None):
        self.api_url = api_url
        self.ws = None
        self.loop = loop
        self.event_callback = event_callback

    async def connect(self):
        print("connecting")
        if self.ws is None:
            print("opening socket")
            self.ws = await websockets.connect(self.api_url)
        print(self.ws)

    async def disconnect(self):
        pass

    async def send(self, message):
        pass

    async def receive(self):
        print("receive started")
        if self.ws is None:
            await self.connect()
        recv_data = await self.ws.recv()
        print(recv_data)
        await self.receive()

    async def start(self):
        print("Started")
        asyncio.gather(self.receive(), loop=self.loop)
        asyncio.set_event_loop(self.loop)

    def stop(self):
        pass

    # async def device_list(self):
    #     print("function "+self.api_url)
    #     # url_connect = "ws://192.168.1.2:7681/root/" + password
    #     async with websockets.connect(self.api_url) as ws:
    #         name = str(
    #             '{"MobileInternalIndex":"231234","CommandType":"DeviceList"}')
    #         await ws.send(name)
    #         # print(f"> {name}")
    #         greeting = await ws.recv()
    #         print()
    #         print(f"< {greeting}")
    #         print()
    #         await ws.send(name)
    #         greeting = await ws.recv()
    #         print()
    #         print(f"< {greeting}")
    #         print()
    #         jsontest = json.loads(greeting)
    #         print(jsontest['Devices'])


#
# def readyaml():
#     with open('./secrets.yaml') as fp:
#         my_configuration_dict = yaml.load(fp)
#     fp.close
#     return my_configuration_dict

# def main():
#     print("Start")
#     my_configuration_dictt = readyaml()
#     securfi_password = my_configuration_dictt["securifi_password"]
#     asyncio.get_event_loop().run_until_complete(devicelist(securfi_password))
#
#
# if __name__ == '__main__':
#     main()
#
# """Main module."""

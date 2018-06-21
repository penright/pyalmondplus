# -*- coding: utf-8 -*-
import asyncio
import websockets
import json


class PyAlmondPlus:

    api_url = None

    def __init__(self, api_url):
        self.api_url = api_url
        print("Start")
        asyncio.get_event_loop().run_until_complete(PyAlmondPlus.device_list(self))

    async def device_list(self):
        # url_connect = "ws://192.168.1.2:7681/root/" + password
        async with websockets.connect(self.api_url) as ws:
            name = str(
                '{"MobileInternalIndex":"231234","CommandType":"DeviceList"}')
        await ws.send(name)
        # print(f"> {name}")
        greeting = await ws.recv()
        print()
        print(f"< {greeting}")
        print()
        await ws.send(name)
        greeting = await ws.recv()
        print()
        print(f"< {greeting}")
        print()
        jsontest = json.loads(greeting)
        print(jsontest['Devices'])


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

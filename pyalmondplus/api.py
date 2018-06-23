# -*- coding: utf-8 -*-
import asyncio
import websockets
import json


class PyAlmondPlus:

    api_url = None
    email_id = None

    def __init__(self, api_url):
        self.api_url = api_url
        print("Start")
        print("start" + self.api_url)
        asyncio.get_event_loop().run_until_complete(PyAlmondPlus.device_list(self))

    async def device_list(self):
        print("function "+self.api_url)
        # url_connect = "ws://192.168.1.2:7681/root/" + password
        async with websockets.connect(self.api_url) as ws:
            name = str(
                '{"MobileInternalIndex":"231234","CommandType":"DeviceList"}')
            await ws.send(name)
            device_header_info = json.loads(await ws.recv())
            self.email_id = (device_header_info['EmailId'])
            await ws.send(name)
            device_detail_info = json.loads(await ws.recv())['Devices']
            print(len(device_detail_info))
            #print(json.dumps(device_detail_info))
            for key in device_detail_info:
                value = device_detail_info[key]
                print("The key and value are ({}) = ({})".format(key, value['Data']['Name']))

class AlmondPlusEntity:
    def __index__(self, almondplus_device):
        self.ID = almondplus_device["ID"]
        self.Name = almondplus_device("Name")
        self.FriendlyDeviceType = almondplus_device["FriendlyDeviceType"]
        self.Type = almondplus_device["Type"]
        self.Location = almondplus_device["Location"]
        self.LastActiveEpoch = almondplus_device["LastActiveEpoch"]
        self.Model = almondplus_device["Model"]
        self.Version = almondplus_device["Version"]
        self.Manufacturer = almondplus_device["Manufacturer"]
        self.device_value_count = len(almondplus_device["DeviceValues"])


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

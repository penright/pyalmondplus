# -*- coding: utf-8 -*-
import threading
import websocket
import uuid
import json
import time


class PyAlmondPlus:

    def __init__(self, api_url, call_back=None):
        self.api_url = api_url
        self.ws = None
        self.call_back = call_back
        self.receive_task = None
        self.last_dym_upate = ""
        self.keep_running = True
        self.client_running = False
        self.send_receive = {}
        self.entity_list = []
        t = threading.Thread(target=self.api_dispatcher, args=())
        t.start()

    def __del__(self):
        print("Delete started")
        if self.ws is not None:
            self.stop()
        print("deleted")

    def connect(self):
        print("connecting")
        if self.ws is None:
            print("opening socket ("+self.api_url+')')
            self.ws = websocket.WebSocket()
            self.ws.connect(self.api_url)
            print("Socket connected")

    def disconnect(self):
        pass

    def _send_receive(self, message):
        pass

    def get_device_list(self):
        tmp_uuid = str(uuid.uuid1())
        my_message = '{"MobileInternalIndex":"' + tmp_uuid + '","CommandType":"DeviceList"}'
        self.send(my_message)
        loop_count = 0
        self.entity_list.clear()
        while loop_count < 20:
            loop_count += 1
            print("loop_count: " + str(loop_count))
            if tmp_uuid in self.send_receive:
                tmp_resp = self.send_receive[tmp_uuid]["Devices"]
                del self.send_receive[tmp_uuid]
                for key in tmp_resp:
                    tmp_device_data = tmp_resp[key]["Data"]
                    tmp_device_value = tmp_resp[key]["DeviceValues"]
                    for device_key in tmp_device_value:
                        self.entity_list.append(AlmondPlusEntity(key, tmp_device_data, device_key
                                                                 , tmp_device_value[device_key]))
                break
            time.sleep(.5)
        print("entity len: "+str(len(self.entity_list)))
        return self.entity_list

    def set_device(self, id, device_id, value):
        print(id + " " + device_id + " "+value)
        message = '{"MobileInternalIndex":"123", "CommandType":"UpdateDeviceIndex", "ID":"' \
                  + id + '","Index":"' + device_id + '", "Value":"' + value + '"}'
        self.send(message)
        #{"MobileInternalIndex": "123", "CommandType": "UpdateDeviceIndex", "ID": "9", "Index": "1", "Value": "true"}

    def send(self, message):
        print("sending "+message)
        self.ws.send(message)
        print("Sent")

    def receive(self):
        print("receive started")
        try:
            recv_data = self.ws.recv()
            print(recv_data)
            parse_data = json.loads(recv_data)
            if 'MobileInternalIndex' in parse_data:
                tmp_mobile_internal_index = parse_data['MobileInternalIndex']
                self.send_receive[tmp_mobile_internal_index] = parse_data
                print("load send rec: " + tmp_mobile_internal_index + '-' + json.dumps(self.send_receive[tmp_mobile_internal_index]))
            elif 'CommandType' in parse_data:
                if self.call_back is not None:
                    self.call_back(json.dumps(parse_data))
                print(parse_data['CommandType'])

        except Exception as e:
            print("Error")
            print("**************************\n"
                  + str(e) + "\n"
                  + "**************************")
            self.ws = None
            return
        print("receive ended")
        if self.client_running:
            self.receive()

    def api_dispatcher(self):
        while self.keep_running:
            print("Dispatcher Start")
            if self.client_running:
                print("Client is running")
                if self.ws is None:
                    print("self.ws is none")
                    self.connect()
                    self.receive()

    def start(self):
        self.client_running = True

    def stop(self):
        print("Stop 1")
        self.client_running = False
        self.keep_running = False
        if self.ws is not None:
            self.ws.close()
            self.ws = None
        print("Stop 2")


class AlmondPlusEntity:
    def __init__(self, data_key, data, device_key, device):
        self.id = data_key
        self.device_id = device_key
        self.name = data["Name"]
        self.friendly_device_type = data["FriendlyDeviceType"]
        self.type = data["Type"]
        self.location = data["Location"]
        self.last_active_epoch = data["LastActiveEpoch"]
        self.model = data["Model"]
        self.value_name = device["Name"]
        self.value_value = device["Value"]
        self.value_type = device["Type"]

# {
#   "MobileInternalIndex":"9cfd3f18-8467-11e8-bbd0-0023246df72f",
#   "CommandType":"DeviceList",
#   "Devices" : {
#               "2":{
#                   "Data":{
#                         "ID":"2",
#                         "Name":"Under Cabinet MultiSwitch",
#                         "FriendlyDeviceType":"BinarySwitch",
#                         "Type":"43",
#                         "Location":"Under Cabinet",
#                         "LastActiveEpoch":"1531220046",
#                         "Model":"Unknown: type=2017,",
#                         "Version":"4",
#                         "Manufacturer":"YALE"
#                         },
#                   "DeviceValues":{
#                                   "1":{
#                                       "Name":"SWITCH_BINARY1",
#                                       "Value":"false",
#                                       "Type":"1"
#                                       },
#                                   "2":{
#                                       "Name":"SWITCH_BINARY2",
#                                       "Value":"false",
#                                       "Type":"1"
#                                       }
#                                 }
#                   },
#               "4":{
#                   "Data":{
#                         "ID":"4",
#                         "Name":"GarageDoorOpener Two Car",
#                         "FriendlyDeviceType":"GarageDoorOpener",
#                         "Type":"53",
#                         "Location":"Default",
#                         "LastActiveEpoch":"1531243088",
#                         "Model":"Unknown: type=4744,",
#                         "Version":"0",
#                         "Manufacturer":"Linear"
#                         },
#                   "DeviceValues":{
#                                   "1":{
#                                       "Name":"BARRIER OPERATOR",
#                                       "Value":"0",
#                                       "Type":"44"
#                                       }
#                                 }
#                   },"5":{"Data":{"ID":"5","Name":"Garage Lights Inside/Outside","FriendlyDeviceType":"BinarySwitch","Type":"43","Location":"Default","LastActiveEpoch":"1531219310","Model":"Unknown: type=2017,","Version":"4","Manufacturer":"YALE"},"DeviceValues":{"1":{"Name":"SWITCH_BINARY1","Value":"false","Type":"1"},"2":{"Name":"SWITCH_BINARY2","Value":"false","Type":"1"}}},"6":{"Data":{"ID":"6","Name":"Vaulted Ceiling/Porch Light","FriendlyDeviceType":"BinarySwitch","Type":"43","Location":"Default","LastActiveEpoch":"1530761308","Model":"Unknown: type=2017,","Version":"4","Manufacturer":"YALE"},"DeviceValues":{"1":{"Name":"SWITCH_BINARY1","Value":"false","Type":"1"},"2":{"Name":"SWITCH_BINARY2","Value":"false","Type":"1"}}},"7":{"Data":{"ID":"7","Name":"Almond Click Purp","FriendlyDeviceType":"SecurifiButton","Type":"61","Location":"Default","LastActiveEpoch":"1531191308","Model":"ZB2-BU01 ","Version":"0","Manufacturer":"Securifi L"},"DeviceValues":{"1":{"Name":"PRESS","Value":"3","Type":"91"},"2":{"Name":"LOW BATTERY","Value":"false","Type":"12"},"3":{"Name":"TAMPER","Value":"false","Type":"9"}}},"8":{"Data":{"ID":"8","Name":"Outside outlet Entryway","FriendlyDeviceType":"BinarySwitch","Type":"1","Location":"Default","LastActiveEpoch":"1531220050","Model":"Unknown: type=2017,","Version":"4","Manufacturer":"YALE"},"DeviceValues":{"1":{"Name":"SWITCH BINARY","Value":"false","Type":"1"}}},"9":{"Data":{"ID":"9","Name":"Power Strip 1","FriendlyDeviceType":"BinarySwitch","Type":"1","Location":"Default","LastActiveEpoch":"1531242749","Model":"ZFM-80","Version":"4","Manufacturer":"Remotec"},"DeviceValues":{"1":{"Name":"SWITCH BINARY","Value":"false","Type":"1"}}}}
# }
#

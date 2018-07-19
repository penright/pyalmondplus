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
        self.entity_dict = AlmondPlusEntityList()
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
        """
        The function will wrap the 'message' with a unique identifier,
            send the message and wait for the response.
        All messages sent will receive a response. That response may indicate success,
            but that is only success for receiving the message. Any command to change the
            state of a device will only know if it is successful when a dynamic message is recived.
            So only 'DeviceList' response really contains useful data.
        :param message:
        'message' is a string of a CommandType and nay data needed.
        It is a json formatted string. All inner elements must use double quotes.
        :return:
        The response after the message tracking data is removed
        """
        tmp_uuid = str(uuid.uuid1())
        my_message = '{"MobileInternalIndex":"' + tmp_uuid + '",' + message + '}'
        self.send(my_message)
        loop_count = 0
        tmp_resp = ""
        while loop_count < 20:
            loop_count += 1
            print("loop_count: " + str(loop_count))
            if tmp_uuid in self.send_receive:
                print("tmp response: " + json.dumps(self.send_receive[tmp_uuid]))
                tmp_resp = self.send_receive[tmp_uuid]
                del self.send_receive[tmp_uuid]
                break
            time.sleep(.5)
        return tmp_resp

    def get_device_list(self):
        self.entity_dict.clear()
        message = '"CommandType":"DeviceList"'
        tmp_resp = self._send_receive(message)["Devices"]
        for id in tmp_resp:
            tmp_device_data = tmp_resp[id]["Data"]
            tmp_device_value = tmp_resp[id]["DeviceValues"]
            for device_id in tmp_device_value:
                tmp_entity = AlmondPlusEntity(tmp_device_data
                                              , device_id
                                              , tmp_device_value[device_id])
                self.entity_dict.append(tmp_entity)
        return self.entity_dict

    def set_device(self, id, device_id, value):
        message = '"CommandType":"UpdateDeviceIndex", "ID":"' \
                  + id + '","Index":"' + device_id + '", "Value":"' + value + '"'
        response = self._send_receive(message)["Success"]
        return response.lower() == 'true'

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


class AlmondPlusEntityList:
    def __init__(self):
        self._EntityDict = {}
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index >= len(self._EntityDict):
            raise StopIteration
        return self._EntityDict.get(list(self._EntityDict.keys())[self._index])

    def __str__(self):
        for key in self._EntityDict:
            return '{"' + key + '":"AlmondPlusEntity:"' + str(self._EntityDict[key]) + '"}'

    def __len__(self):
        return len(self._EntityDict)

    def clear(self):
        self._EntityDict.clear()

    def append(self, value):
        self._EntityDict[value.id.zfill(4)+value.device_id.zfill(4)] = value

    def get(self, id, device_id):
        return self._EntityDict[id.zfill(4)+device_id.zfill(4)]

    def exist(self, id, device_id):
        return id.zfill(4)+device_id.zfill(4) in self._EntityDict.keys()


class AlmondPlusEntity:
    def __init__(self, device_data, device_id, device_values):
        self.id = device_data["ID"]
        self.device_id = device_id
        self.name = device_data["Name"]
        self.friendly_device_type = device_data["FriendlyDeviceType"]
        self.type = device_data["Type"]
        self.location = device_data["Location"]
        self.last_active_epoch = device_data["LastActiveEpoch"]
        self.model = device_data["Model"]
        self.value_name = device_values["Name"]
        self.value_value = device_values["Value"]
        self.value_type = device_values["Type"]

    def __str__(self):
        return '{' \
                + '"id":"' + self.id + '"' \
                + ',"device_id":"' + self.device_id + '"' \
                + ',"name":"' + self.name + '"' \
                + ',"friendly_device_type":"' + self.friendly_device_type + '"' \
                + ',"location":"' + self.location + '"' \
                + ',"last_active_epoch":"' + self.last_active_epoch + '"' \
                + ',"model":"' + self.model + '"' \
                + ',"value_name":"' + self.value_name + '"' \
                + ',"value_value":"' + self.value_value + '"' \
                + ',"value_type":"' + self.value_type + '"' \
                + '}'

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

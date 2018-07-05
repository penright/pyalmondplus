# -*- coding: utf-8 -*-
import threading
import asyncio
import websockets
import json
#This is to test merg #30

class PyAlmondPlus:

    def __init__(self, api_url, event_callback=None):
        self.api_url = api_url
        self.ws = None
        self.loop = asyncio.get_event_loop()
        self.receive_task = None
        self.event_callback = event_callback
        self.keep_running = True
        self.client_running = False
        t = threading.Thread(target=self.api_dispatcher, args=())
        t.start()

    async def connect(self):
        print("connecting")
        if self.ws is None:
            print("opening socket")
            self.ws = await websockets.connect(self.api_url)
        print(self.ws)

    async def disconnect(self):
        pass

    def get_device_list(self):
        my_message = '{"MobileInternalIndex":"231234","CommandType":"DeviceList"}'
        self.send(my_message)

    def send(self, message):
        print("sending "+message)
        self.ws.send(message)

    async def receive(self):
        print("receive started")
        while self.keep_running:
            if self.ws is None:
                await self.connect()
            recv_data = await self.ws.recv()
            print(recv_data)
        print("receive ended")

    async def api_dispatcher(self):
        while self.keep_running:
            print("Before sleep")
            asyncio.sleep(1000)
            print("After sleep")
            if self.client_running:
                if self.ws is None:
                    await self.connect()


    def start(self):
        self.keep_running = True

    def start_loop(self):
        print("Loop helper 1")
        policy = asyncio.get_event_loop_policy()
        policy.set_event_loop(policy.new_event_loop())
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.api_dispatcher())
        print("Loop helper 2")

    def stop(self):
        print("Stop 1")
        self.keep_running = False
        print("Stop 2")
        self.ws.close()
        print("Stop 3")


# class testingThread(threading.Thread):
#     def __init__(self,threadID):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#     def run(self):
#         print str(self.threadID) + " Starting thread"
#         self.ws = websocket.WebSocketApp("ws://localhost/ws", on_error = self.on_error, on_close = self.on_close, on_message=self.on_message,on_open=self.on_open)
#         self.ws.keep_running = True
#         self.wst = threading.Thread(target=self.ws.run_forever)
#         self.wst.daemon = True
#         self.wst.start()
#         running = True;
#         testNr = 0;
#         time.sleep(0.1)
#         while running:
#             testNr = testNr+1;
#             time.sleep(1.0)
#             self.ws.send(str(self.threadID)+" Test: "+str(testNr)+")
#         self.ws.keep_running = False;
#         print str(self.threadID) + " Exiting thread"





# # -*- coding: utf-8 -*-
# import asyncio
# import websockets
# import json
#
#
# class PyAlmondPlus:
#
#     def __init__(self, api_url, event_callback=None):
#         self.api_url = api_url
#         self.ws = None
#         self.receive_task = None
#         self.event_callback = event_callback
#         self.receive_running = False
#         self.loop = None
#
#     def connect(self):
#         print("connecting")
#         if self.ws is None:
#             print("opening socket "+self.api_url)
#             self.ws = websockets.connect(self.api_url)
#         print(self.ws)
#
#     def disconnect(self):
#         pass
#
#     def send(self, message):
#         pass
#
#     def receive(self):
#         print("receive started")
#         if self.ws is None:
#             self.connect()
#         while self.receive_running:
#             recv_data = self.ws.recv()
#             print(recv_data)
#
#     def start(self):
#         print("Start Thread loop")
#         self.receive_running = True
#         import threading
#         self.receive_task = threading.Thread(target=self.receive, args=())
#         self.receive_task.start()
#         print("Receiver running")
#
#     def stop(self):
#         print("Stop Reciver")
#         self.receive_running = False
#
# # -*- coding: utf-8 -*-
# import asyncio
# import websockets
# import json
#
#
# class PyAlmondPlus:
#
#     def __init__(self, api_url, event_callback=None):
#         self.api_url = api_url
#         self.ws = None
#         self.loop = asyncio.get_event_loop()
#         self.event_callback = event_callback
#         self.keep_running = False
#
#     async def connect(self):
#         print("connecting")
#         if self.ws is None:
#             print("opening socket "+self.api_url)
#             self.ws = await websockets.connect(self.api_url)
#         print(self.ws)
#
#     async def disconnect(self):
#         pass
#
#     async def send(self, message):
#         pass
#
#     async def receive(self):
#         print("receive started")
#         if self.ws is None:
#             await self.connect()
#         while self.keep_running:
#             recv_data = await self.ws.recv()
#             print(recv_data)
#         print("receive stopped")
#
#     def start(self):
#         print("Start 1")
#         self.keep_running = True
#         asyncio.ensure_future(self.receive, loop=self.loop)
#         print("Start 2")
#
#     def stop(self):
#         print("Stop 1")
#         self.keep_running = False
#         self.ws.keep_running = False

#___________________________________________________________

#
#     # async def device_list(self):
#     #     print("function "+self.api_url)
#     #     # url_connect = "ws://192.168.1.2:7681/root/" + password
#     #     async with websockets.connect(self.api_url) as ws:
#     #         name = str(
#     #             '{"MobileInternalIndex":"231234","CommandType":"DeviceList"}')
#     #         await ws.send(name)
#     #         # print(f"> {name}")
#     #         greeting = await ws.recv()
#     #         print()
#     #         print(f"< {greeting}")
#     #         print()
#     #         await ws.send(name)
#     #         greeting = await ws.recv()
#     #         print()
#     #         print(f"< {greeting}")
#     #         print()
#     #         jsontest = json.loads(greeting)
#     #         print(jsontest['Devices'])
#
#
# #
# # def readyaml():
# #     with open('./secrets.yaml') as fp:
# #         my_configuration_dict = yaml.load(fp)
# #     fp.close
# #     return my_configuration_dict
#
# # def main():
# #     print("Start")
# #     my_configuration_dictt = readyaml()
# #     securfi_password = my_configuration_dictt["securifi_password"]
# #     asyncio.get_event_loop().run_until_complete(devicelist(securfi_password))
# #
# #
# # if __name__ == '__main__':
# #     main()
# #
# # """Main module."""
pass


from channels.generic.websocket import AsyncWebsocketConsumer
import json
import sys
import threading
import objgraph 
import asyncio

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # async 关键字 将生成器转化为 协程 类型
        self.room_group_name = 'chat_video'

        # join room group
        # await 关键字
        # 1 执行 await 右边方法，返回产出值 如 a = await a()
        # 2 同时 connecct() 阻塞
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 离开群组
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
    
    # 1.1 接收来自 Websocket 的字节消息 bytes_data，文本消息 text_data
    async def receive(self, bytes_data):
        print(sys.getsizeof(bytes_data))
        # text_data_json = json.loads(text_data)
        # print('这是python连接websocket ',text_data_json)
        # image = text_data_json['image']
        # print('user ??: ', vars(self.scope["user"]))
        # image = bytes_data
        # 1.2 向 group 发送信息
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.video',
                'image': bytes_data,
            }
        )
    
    # 2.1 接收来自 group 的信息
    async def chat_video(self, event):
        # print(type(self.send))
        # # pass
        # import time
        # time.sleep(1)
        # 2.2 向 WebSocket 发送消息
        # await self.send(bytes_data=b'image')
        await self.send(bytes_data=event['image'])
    
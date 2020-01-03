# 2 consumer 的异步写法
"""以下几点不同
 1 ChatConsumer 从 AsyncWebsocketConsumer 继承
 2 所有方法变成 协程 类型（async 异步）
 3 await 用来调用需执行 I/O 的方法
 4 不需要使用 async_to_sync
"""
# 请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：
# 1 把@asyncio.coroutine替换为async；
# 2 把yield from替换为await。
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async # 数据库操作
from chat.models import GroupMessage
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # async 关键字 将生成器转化为 协程 类型
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
    
    # 接收来自 Websocket 的消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 异步调用数据库
        self.message = message
        time = await database_sync_to_async(self.create_log)(1) # 不加装饰器的写法
        # time = await self.create_log(1) # 加装饰器的写法
        print('user ??: ', vars(self.scope["user"]), self.scope["user"].username, self.room_name)


        # 向 group 发送信息
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope["user"].username,
                'time': time,
            }
        )
    
    # 接收来自 group 的信息
    async def chat_message(self, event):
        message = event['message']
        time = event['time']
        sender = event['sender']

        # 向 WebSocket 发送消息
        await self.send(text_data=json.dumps({
            'message':message,
            'sender': sender,
            'time': time,
        }))

    # @database_sync_to_async
    def create_log(self,a):
        """保存消息"""
        gm = GroupMessage.objects.create(user=self.scope["user"],message=self.message,groupname=self.room_name)
        # GroupMessage.objects.all()
        # GroupMessage.objects.get(pk=1)
        print('我接收到消息了',a)
        return str(gm.create_time)


# 1 consumer 的同步写法

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# import json

# class ChatConsumer(WebsocketConsumer):
#     """
#      1 所有的 channel layer 方法都是异步的
#     """
#     def connect(self):
#         # chat/routing.py 中包含的 room_name 参数
#         # 每一个 consumer 都有 scope 包含连接的信息，包含
#         # chat/routing.py 中的位置参数、关键词参数，和当前
#         # 认证的用户信息
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         # 接受 WebSocket 方法，并在连接的最后调用
#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         # 将 事件 发送给 group
#         # 事件会有特殊的 type 键对应在接收事件中
#         # consumer 应该对应的方法。
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
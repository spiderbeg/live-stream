from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path, path

from chat.consumers import ChatConsumer 
from video.consumers import VideoConsumer


application = ProtocolTypeRouter({
    # (http->Django views is add by default)
    # https://channels.readthedocs.io/en/latest/releases/2.1.0.html?highlight=URLRouter#nested-url-routing
    'websocket': AuthMiddlewareStack(
      URLRouter(
        [
          path('ws/chat/<str:room_name>/', ChatConsumer),
          path('ws/video/', VideoConsumer),
        ]
        ) # 与 Django include() 相似
    ),
})
""" 上面 根路由配置含义
 1 指定当连接发向 Channels 开发服务，ProtocolTypeRouter 检测
   协议类型，如果是 Websocket 连接（ws:// 或 wss://），连接将
   会给到 AuthMiddlewareStack。
 2 AuthMiddlewareStack 将引用认证用户来构成连接的一部分，与 Django
   AuthenticationMiddleware 相似。接下来连接会给到 URLRouter。
 3 URLRouter 根据提供的 url pattern 决定 HTTP 连接的路径指向哪一个 
   consumer.

"""
""" channel layer（通道层） 
 1 channel layer 是一种通信系统。它允许多消费实例之间或者
   与 Django 其他互相部分通信。
 2 channel layer 提供以下抽象：
   1 类似于接收信息的邮箱，每一个 channel 有自己的名字。任何有 channel 
     名字的人都可以向 channel 发送信息。
   2 一个群组是相互关联的 channel 的群组。一个群组有自己的名字。任何有 群组
     名字的人可以通过 channel 的名字添加或移除群组中的 channel；并且可以向群组
     中的所有 channel 发送消息。
     不可以枚举出一个群组中有哪些 channel。
 3 每一个消费者实例都会自动生成一个独一无二的 channel 名字，以用于 channel layer
   通信。
 4 在我们的聊天应用中，我们希望一个聊天室中可以存在多个实例之间相互交流。
   为了做到这一点我们需要每一个 ChatConsumer 添加相同房间名的 channel 到一个群组。
   这将会允许所有同一个房间的 ChatConsumers 可以向其他实例传输信息。
   
"""
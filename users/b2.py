# encoding:utf8
import asyncio
import websockets
import json
import time
import numpy as np
import cv2
import sys

async def receive_video(uri):
    async with websockets.connect(uri,max_queue=2**10,read_limit=2**18,write_limit=2**18) as websocket:
        while True:
            message = await websocket.recv()
            # print(sys.getsizeof(message))
            image = np.asarray(bytearray(message), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cv2.imshow('image',image)
            if cv2.waitKey(1) & 0xFF == ord('q'): # 获取到键盘按下 'q' 键
                break
        
    # 最后，释放占用的摄像机资源
    cv2.destroyAllWindows()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        receive_video('ws://127.0.0.1:8000/ws/video/'))
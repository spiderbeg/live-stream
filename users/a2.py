# encoding:utf8
import asyncio
import websockets
import json
import time
import numpy as np
import cv2
import sys
import os
import threading
import concurrent.futures
import redis
import pickle

# 传输每一帧的图片信息

def save_image():
    '''
    opencv 调用摄像头并将每一帧图片保存为 jpg 模式。
    '''
    cap = cv2.VideoCapture(0) # 一般对于电脑来说 0，就是代表自带的摄像头设备
    cap.set(3,480)
    cap.set(4,360)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90] # 压缩参数
    while cap.isOpened():
        # 逐帧获取图片
        ret, frame = cap.read() # ret: 布尔值，表示是否读取正确；frame：图片信息 
        # 将图片解码为 jpg 格式
        _, encoded_image = cv2.imencode('.jpg', frame, encode_param) # 有损压缩
        content2 = encoded_image.tobytes() # 转换为字节
        # print('size of compress image', sys.getsizeof(content2))
        lock.acquire()
        r.set('image',content2) # 存储到 redis
        lock.release()
        # 展示结果
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # 获取到键盘按下 'q' 键
                break
        time.sleep(0.05)
    # 最后，释放占用的摄像机资源
    cap.release()
    cv2.destroyAllWindows()

async def send_video(uri):
    '''
    从缓存中获取 jpg 图片二进制信息，并上传到服务器
    '''
    async with websockets.connect(uri,max_queue=2**10,read_limit=2**18,write_limit=2**18) as websocket:
        time.sleep(2) # opencv 启动时间停顿
        while True:            
            lock.acquire()
            img = r.get('image')
            lock.release()
            # print(type(img))
            if type(img) == type(None): # 防止 redis 中数据为空
                continue
            time.sleep(0.08)
            print(sys.getsizeof(img))
            await websocket.send(img)
            # break

if __name__ == '__main__':
    # 连接 redis ，设置缓存时长
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.expire('image', 1)
    # 线程锁
    lock=threading.Lock()
    # 开启视频录制线程
    t = threading.Thread(target=save_image)
    # 设置守护线程。当没有存活的非守护线程，程序退出
    t.daemon = True
    t.start()

    # 开启协程主事件循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        send_video('ws://127.0.0.1:8000/ws/video/'))


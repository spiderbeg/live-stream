from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
import json

# Create your views here.
@login_required
def index(request):
    # import time
    # import threading
    # 测试一下 视图中使用多线程，
    # def doWaiting():
    #     print('start waiting:', time.strftime('%H:%M:%S'))
    #     time.sleep(3)
    #     print('stop waiting', time.strftime('%H:%M:%S'))
    # t = threading.Thread(target=doWaiting)
    # t.start()

    return render(request, 'chat/index.html',{})

def room(request, room_name):
    return render(request, 'chat/room.html',{
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def getLogin(request):
    """重定向至登录页面"""
    return redirect('chat:index')

def getLogout(request):
    """重定向至登录页面"""
    logout(request) # 登出
    return redirect('chat:index')

def signup(request):#用户注册
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 用户注册，返回用户对象
            login(request, user) # 执行登录过程
            return redirect('chat:index')
    else:
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form':form})
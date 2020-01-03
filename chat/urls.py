from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('signup/', views.signup, name="signup"),
    path('getLogout/', views.getLogout, name="getLogout"),
    path('getLogin/', views.getLogin, name="getLogin"),
]

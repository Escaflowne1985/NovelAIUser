# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = ''

from django.urls import path
from .views import *

urlpatterns = [
    path('Movie_Step_View', Movie_Step_View.as_view(), name='Movie_Step_View'),
    path('Movie_Step_Task_View/<int:num>', Movie_Step_Task_View.as_view(), name='Movie_Step_Task_View'),
    path('Movie_Step_1_View/<int:num>', Movie_Step_1_View.as_view(), name='Movie_Step_1_View'),
    path('Movie_Step_2_View/<int:num>', Movie_Step_2_View.as_view(), name='Movie_Step_2_View'),
    path('Movie_Step_3_View/<int:num>', Movie_Step_3_View.as_view(), name='Movie_Step_3_View'),
    path('Movie_Step_4_View/<int:num>', Movie_Step_4_View.as_view(), name='Movie_Step_4_View'),
    path('Movie_Step_Each_1_View//<int:num>/<int:index>', Movie_Step_Each_1_View.as_view(), name='Movie_Step_Each_1_View'),
    path('Movie_Step_Each_2_View/<int:num>/<int:index>', Movie_Step_Each_2_View.as_view(), name='Movie_Step_Each_2_View'),

]

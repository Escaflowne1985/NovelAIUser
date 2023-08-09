# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = ''

from django.urls import path
from .views import *

urlpatterns = [
    path('Video_Step_View', Video_Step_View.as_view(), name='Video_Step_View'),
    path('Video_Step_Base_View', Video_Step_Base_View.as_view(), name='Video_Step_Base_View'),
    path('Video_Step_Insert_View', Video_Step_Insert_View.as_view(), name='Video_Step_Insert_View'),
    path('Video_Step_Add_View', Video_Step_Add_View.as_view(), name='Video_Step_Add_View'),
    path('Video_Step_RandomCut_View', Video_Step_RandomCut_View.as_view(), name='Video_Step_RandomCut_View'),
]

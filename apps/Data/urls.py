# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = ''

from django.urls import path
from .views import *

urlpatterns = [
    path('New_Step_1_View', New_Step_1_View.as_view(), name='New_Step_1_View'),
    path('Step_1_1_View/', Step_1_1_View.as_view(), name='Step_1_1_View'),
    path('New_Step_2_View', New_Step_2_View.as_view(), name='New_Step_2_View'),
    path('New_Step_2_Process_View/<int:num>', New_Step_2_Process_View.as_view(), name='New_Step_2_Process_View'),
    path('Step_2_1_View/<int:num>', Step_2_1_View.as_view(), name='Step_2_1_View'),
    path('Step_2_2_View/<int:num>', Step_2_2_View.as_view(), name='Step_2_2_View'),
    path('Step_2_3_View/<int:num>', Step_2_3_View.as_view(), name='Step_2_3_View'),
    path('Step_2_4_View/<int:num>', Step_2_4_View.as_view(), name='Step_2_4_View'),
    path('New_Step_3_View', New_Step_3_View.as_view(), name='New_Step_3_View'),
    path('New_Step_3_Process_View/<int:num>', New_Step_3_Process_View.as_view(), name='New_Step_3_Process_View'),
    path('Step_4_1_View/<int:num>', Step_4_1_View.as_view(), name='Step_4_1_View'),
    path('Step_4_2_View/<int:num>/<int:index>', Step_4_2_View.as_view(),name='Step_4_2_View'),
    path('Step_4_3_View/<int:num>/<int:index>', Step_4_3_View.as_view(), name='Step_4_3_View'),
    path('Step_4_4_View/<int:num>/<int:index>', Step_4_4_View.as_view(), name='Step_4_4_View'),
    path('Step_4_5_View/<int:num>', Step_4_5_View.as_view(), name='Step_4_5_View'),
    path('Step_2_All_View/', Step_2_All_View.as_view(), name='Step_2_All_View'),
    path('Step_3_All_View/', Step_3_All_View.as_view(), name='Step_3_All_View'),
    path("ReDraw/", ReDraw, name='ReDraw'),
    path("Prompt/", Prompt, name='Prompt'),
    path("Prompt_View", Prompt_View.as_view(), name='Prompt_View'),
]

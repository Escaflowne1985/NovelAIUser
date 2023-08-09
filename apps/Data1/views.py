from django.shortcuts import render
from django.views.generic.base import View
from Config.models import *

try:
    from apps.Utils.script.video_step_base import *
except:
    from apps.Utils.pyd.video_step_base import *


class Video_Step_View(View):
    def get(self, request):
        return render(request, 'Video_Step_Base.html', locals())


class Video_Step_Base_View(View):
    def get(self, request):
        video_base_function()
        return render(request, 'Video_Step_Base.html', locals())

class Video_Step_Insert_View(View):
    def get(self, request):
        video_base_insert_function()
        return render(request, 'Video_Step_Base.html', locals())

class Video_Step_Add_View(View):
    def get(self, request):
        video_base_add_function()
        return render(request, 'Video_Step_Base.html', locals())
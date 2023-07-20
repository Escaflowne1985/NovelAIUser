from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *
from django.shortcuts import redirect
from Config.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse

try:
    from .script.new_step1 import *
except:
    from .pyd.new_step1 import *
try:
    from .script.new_step2 import *
except:
    from .pyd.new_step2 import *
try:
    from .script.step1 import *
except:
    from .pyd.step1 import *
try:
    from .script.step2 import *
except:
    from .pyd.step2 import *
try:
    from .script.step3 import *
except:
    from .pyd.step3 import *
try:
    from .script.step4 import *
except:
    from .pyd.step4 import *
try:
    from .script.new_step3 import *
except:
    from .pyd.new_step3 import *
try:
    from .script.new_redraw import *
except:
    from .pyd.new_redraw import *
try:
    from .script.prompt import *
except:
    from .pyd.prompt import *


# 设置全局TEMPLATES变量用于每个页面使用
def GlobalInit(request):
    task = Task.objects.all().values('id', 'type', 'en_name', 'cn_name', 'len_text')
    task_list = Task.objects.filter(status="未完成")
    lora_list = LoraModels.objects.all()
    return locals()


# 主页Home数据
def Home(request):
    return render(request, 'base.html', locals())


class New_Step_1_View(View):
    def get(self, request):
        return render(request, 'New_Step_1.html', locals())

    def post(self, request):
        step_1_lora_fuction(request)
        return redirect('New_Step_1_View')


class Step_1_1_View(View):
    def get(self, request):
        task_id = request.GET.get('task_id')
        task_data = Task.objects.filter(id=int(task_id))[0]
        step_3_1_fuction(task_id)
        json_content_start = eval(Task.objects.filter(id=task_id)[0].content_start_json)
        json_content_start = [i for i in json_content_start if len(i)]
        return render(request, 'New_Step_1.html', locals())

    def post(self, request):
        task_id = request.POST.get('task_id_')
        content_start = request.POST.get('content_start')
        Task.objects.filter(id=int(task_id)).update(content_start=content_start)
        return render(request, 'New_Step_1.html', locals())


class New_Step_2_View(View):
    def get(self, request):
        return render(request, 'New_Step_2.html', locals())


class Step_2_1_View(View):
    def get(self, request, num):
        step_1_fuction(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class Step_2_2_View(View):
    def get(self, request, num):
        step_2_fuction(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class Step_2_3_View(View):
    def get(self, request, num):
        step_3_fuction(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class Step_2_4_View(View):
    def get(self, request, num):
        step_4_fuction(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class New_Step_2_Process_View(View):
    def get(self, request, num):
        step_2_process(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class Step_2_All_View(View):
    def get(self, request):
        data_list = Task.objects.filter(status="未完成")
        for data in data_list:
            print("开始执行：", data.cn_name)
            num = data.id
            step_2_process(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class New_Step_3_View(View):
    def get(self, request):
        return render(request, 'New_Step_3.html', locals())


class New_Step_3_Process_View(View):
    def get(self, request, num):
        step_3_process(num, Task, TaskEach)
        return render(request, 'New_Step_3.html', locals())


class Step_3_All_View(View):
    def get(self, request):
        data_list = Task.objects.filter(status="未完成")
        for data in data_list:
            print("开始执行：", data.cn_name)
            num = data.id
            step_3_process(num, Task, TaskEach)
        return render(request, 'New_Step_3.html', locals())


def ReDraw(request):
    # print(request.is_login)
    return render(request, 'redraw.html', locals())


# 获取重绘任务数据
class Step_4_1_View(View):
    def get(self, request, num):
        # 获取任务的数据
        task_id = Task.objects.filter(id=num).first().id
        data_list = TaskEach.objects.filter(task_id=task_id).order_by('id')
        return render(request, 'redraw.html', locals())


# 图片重绘
class Step_4_2_View(View):
    def get(self, request, num, index):
        # 获取任务的数据
        task_id = Task.objects.filter(id=num).first().id
        type_path = Task.objects.filter(id=num).first().type
        en_name = Task.objects.filter(id=num).first().en_name
        step_4_2_fuction(num, type_path, en_name, index, Task, TaskEach)
        # return HttpResponseRedirect(request.get_full_path())
        # return render(request, 'redraw.html', locals())
        return redirect(reverse('Step_4_1_View', args=[num]))


# 图片关键词重新生成
class Step_4_3_View(View):
    def get(self, request, num, index):
        step_2_1_fuction(num, index)
        return redirect(reverse('Step_4_1_View', args=[num]))


# 数据保存
class Step_4_4_View(View):
    def post(self, request, num, index):
        txt = request.POST.get('txt')
        prompt = request.POST.get('prompt')
        negative = request.POST.get('negative')
        # 获取要更新的对象
        obj = TaskEach.objects.get(task_id=num, index=index)
        # 更新指定字段
        obj.txt = txt
        obj.prompt = prompt
        obj.negative = negative
        obj.save()
        return redirect(reverse('Step_4_1_View', args=[num]))


def Prompt(request):
    # print(request.is_login)
    # 访问直接获取最后20条数据
    data_list = get_prompt(UserData)
    return render(request, 'Prompt.html', locals())


class Prompt_View(View):
    def post(self, request):
        text = request.POST.get('text', '')  # 获取前端提交的文本数据
        print(text)
        step_prompt(text, UserData)
        return redirect('Prompt')
        # return render(request, 'Prompt.html', locals())

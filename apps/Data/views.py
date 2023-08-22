from django.shortcuts import render
from django.views.generic.base import View
import json
from .models import *
from Data2.models import *
from django.shortcuts import redirect
from Config.models import *
from django.urls import reverse

try:
    from apps.Utils.script.new_step1 import *
except:
    from apps.Utils.pyd.new_step1 import *
try:
    from apps.Utils.script.new_step2 import *
except:
    from apps.Utils.pyd.new_step2 import *
try:
    from apps.Utils.script.step1 import *
except:
    from apps.Utils.pyd.step1 import *
try:
    from apps.Utils.script.step2 import *
except:
    from apps.Utils.pyd.step2 import *
try:
    from apps.Utils.script.step3 import *
except:
    from apps.Utils.pyd.step3 import *
try:
    from apps.Utils.script.step4 import *
except:
    from apps.Utils.pyd.step4 import *
try:
    from apps.Utils.script.new_step3 import *
except:
    from apps.Utils.pyd.new_step3 import *
try:
    from apps.Utils.script.new_redraw import *
except:
    from apps.Utils.pyd.new_redraw import *
try:
    from apps.Utils.script.prompt import *
except:
    from apps.Utils.pyd.prompt import *


# 设置全局TEMPLATES变量用于每个页面使用
def GlobalInit(request):
    task = Task.objects.all().values('id', 'type', 'en_name', 'cn_name', 'len_text')
    task_list = Task.objects.filter(status="未完成")
    lora_list = LoraModels.objects.all()

    task_movie = MovieTask.objects.all().values('id', 'type', 'en_name', 'cn_name')
    task_movie_list = MovieTask.objects.filter(status="未完成")
    return locals()


# 主页Home数据
def Home(request):
    return render(request, 'base.html', locals())


# LoRA人物配置
class New_Step_1_View(View):
    def get(self, request):
        return render(request, 'New_Step_1.html', locals())

    def post(self, request):
        step_1_lora_fuction(request)
        return redirect('New_Step_1_View')


# 黄金文案5秒
class New_Step_1_1_View(View):
    def get(self, request):
        task_id = request.GET.get('task_id')
        task_data = Task.objects.filter(id=int(task_id))[0]
        step_1_gold_start_fuction(task_id)
        json_content_start = eval(Task.objects.filter(id=task_id)[0].content_start_json)
        json_content_start = [i for i in json_content_start if len(i) > 3]
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
        step_1_function(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class Step_2_2_View(View):
    def get(self, request, num):
        step_2_function(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class Step_2_3_View(View):
    def get(self, request, num):
        step_3_function(num, Task, TaskEach)
        return render(request, 'New_Step_2.html', locals())


class Step_2_4_View(View):
    def get(self, request, num):
        step_4_function(num, Task, TaskEach)
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
        return render(request, 'New_Step_2.html', locals())


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
    task_id = 0
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
        step_4_2_function(num, type_path, en_name, index, Task, TaskEach)
        # return HttpResponseRedirect(request.get_full_path())
        # return render(request, 'redraw.html', locals())
        return redirect(reverse('Step_4_1_View', args=[num]))

    def post(self, request, num, index):
        # 获取任务的数据
        task_id = Task.objects.filter(id=num).first().id
        type_path = Task.objects.filter(id=num).first().type
        en_name = Task.objects.filter(id=num).first().en_name
        step_4_2_function(num, type_path, en_name, index, Task, TaskEach)
        # return HttpResponseRedirect(request.get_full_path())
        # return render(request, 'redraw.html', locals())
        return redirect(reverse('Step_4_1_View', args=[num]))


# 图片关键词重新生成
class Step_4_3_View(View):
    def get(self, request, num, index):
        step_2_1_function(num, index)
        return redirect(reverse('Step_4_1_View', args=[num]))

    def post(self, request, num, index):
        step_2_1_function(num, index)
        return redirect(reverse('Step_4_1_View', args=[num]))


# 数据保存
class Step_4_4_View(View):
    def post(self, request, num, index):
        txt = request.POST.get('txt')
        prompt = request.POST.get('prompt')
        negative = request.POST.get('negative')
        lora = request.POST.get('lora')
        lora_add = request.POST.get('lora_add')
        lora_del = request.POST.get('lora_del')
        lora_choose = request.POST.get('lora_choose')
        prefix = request.POST.get('prefix')
        prefix_add = request.POST.get('prefix_add')
        prefix_del = request.POST.get('prefix_del')
        translate_add = request.POST.get('translate_add')

        if txt is not None:
            obj = TaskEach.objects.get(task_id=num, index=index)
            obj.txt = txt
            obj.save()

        if prompt is not None:
            obj = TaskEach.objects.get(task_id=num, index=index)
            obj.prompt = prompt
            obj.save()

        if negative is not None:
            obj = TaskEach.objects.get(task_id=num, index=index)
            obj.negative = negative
            obj.save()

        if lora is not None:
            obj = TaskEach.objects.get(task_id=num, index=index)
            obj.prompt = lora + ',' + obj.prompt
            obj.save()

        if lora_add is not None:
            obj = TaskEach.objects.filter(task_id=num)
            for n in range(len(obj)):
                obj[n].prompt = clean_txt(lora_choose + "," + obj[n].prompt)
                obj[n].save()
                # print(obj[n])

        if lora_del is not None:
            obj = TaskEach.objects.filter(task_id=num)
            for n in range(len(obj)):
                obj[n].prompt = clean_txt(obj[n].prompt.replace(lora_choose, ""))
                obj[n].save()
                # print(obj[n])

        if prefix_add is not None:
            obj = TaskEach.objects.filter(task_id=num)
            for n in range(len(obj)):
                obj[n].prompt = clean_txt(prefix + "," + obj[n].prompt)
                obj[n].save()
                # print(obj[n].prompt)

        if prefix_del is not None:
            obj = TaskEach.objects.filter(task_id=num)
            for n in range(len(obj)):
                obj[n].prompt = clean_txt(obj[n].prompt.replace(prefix, ""))
                obj[n].save()
                # print(obj[n].prompt)

        if translate_add is not None:
            translate_add_translated = ts.translate_text(translate_add, to_language='en')
            obj = TaskEach.objects.get(task_id=num, index=index)
            obj.prompt = obj.prompt + "," + translate_add_translated
            obj.save()

        return redirect(reverse('Step_4_1_View', args=[num]))


# 图片重绘
class Step_4_5_View(View):
    def get(self, request, num):
        # 获取任务的数据
        obj = TaskEach.objects.filter(task_id=num)
        for n in range(len(obj)):
            obj[n].prompt = "待处理"
            obj[n].save()
            print(obj[n])

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


# 关键词翻译功能
from django.http import JsonResponse
import translators as ts


class Translate(View):
    def post(self, request):
        data = json.loads(request.body)
        text = data['text']
        # 执行翻译，这里您可以调用任何翻译库或服务
        translated_text = ts.translate_text(text, to_language='zh')
        # print(translated_text)
        # print("-"*20)

        return JsonResponse({'translatedText': translated_text})

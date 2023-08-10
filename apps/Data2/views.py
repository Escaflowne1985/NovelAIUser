from django.shortcuts import render
from django.views.generic.base import View
from Config.models import *
from .models import *

try:
    from Utils.script.movie_step_base import *
except:
    from Utils.pyd.movie_step_base import *


class Movie_Step_View(View):
    def get(self, request):
        return render(request, 'Movie_Step_Base.html', locals())


# 获取明细任务数据
class Movie_Step_Task_View(View):
    def get(self, request, num):
        # 获取任务的数据
        task_id = MovieTask.objects.filter(id=num).first().id
        data_list = MovieTaskEach.objects.filter(task_id=task_id).order_by('id')
        return render(request, 'Movie_Step_Base.html', locals())


# 生成字幕
class Movie_Step_1_View(View):
    def get(self, request, num):
        make_whisper(request, num)
        return render(request, 'Movie_Step_Base.html', locals())


# GPT洗稿
class Movie_Step_2_View(View):
    def get(self, request, num):
        movie_srt_all_function(num, MovieTask, MovieTaskEach)
        return render(request, 'Movie_Step_Base.html', locals())


# 生成语音
class Movie_Step_3_View(View):
    def get(self, request, num):
        movie_audio_function(num, MovieTask, MovieTaskEach)
        return render(request, 'Movie_Step_Base.html', locals())


# 合并成视频
class Movie_Step_4_View(View):
    def get(self, request, num):
        movie_merge_function(num)
        return render(request, 'Movie_Step_Base.html', locals())


class Movie_Step_Each_1_View(View):
    def post(self, request, num, index):
        txt_new = request.POST.get('txt_new')
        MovieTaskEach.objects.filter(task_id=num, index=index).update(txt_new=txt_new)
        return render(request, 'Movie_Step_Base.html', locals())


class Movie_Step_Each_2_View(View):
    def post(self, request, num, index):
        movie_audio_each_save_function(num, index)
        return render(request, 'Movie_Step_Base.html', locals())


# 删除MovieTaskEach对应的记录和音频文件
class Movie_Step_Each_3_View(View):
    def get(self, request, num, index):
        data_list = MovieTask.objects.filter(id=num).first()
        type_path = data_list.type
        en_name = data_list.en_name

        # 删除记录
        records_to_delete = MovieTaskEach.objects.filter(task_id=num, index=index)
        records_to_delete.delete()

        # 删除制定wav文件
        del_wav_path = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "each_audio_wav", str(index) + ".wav")
        try:
            os.remove(del_wav_path)
        except:
            pass

        return render(request, 'Movie_Step_Base.html')

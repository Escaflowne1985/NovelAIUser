# -*- coding: UTF-8 -*-
import os
from Config.models import *
from Data.models import *
from NovelAIUser.settings import *

try:
    from apps.Utils.script.GeneralTools import *
except:
    from apps.Utils.pyd.GeneralTools import *


def step_1_function(num, Task, TaskEach):
    # 获取用户信息
    result_info = user_authenticate()
    print(result_info["msg"])

    if '用户验证通过' in result_info["msg"]:
        ##### 稿件拆分部分 #####
        data = Task.objects.filter(id=num).first()
        cn_name = data.cn_name
        en_name = data.en_name
        type_path = data.type
        task_id = data.id
        content_start = data.content_start

        # 对content进行断句分割
        content = content_start + "。" + data.content
        content = content.replace('"', "").replace("'", "")
        content = content.split('。')
        content = [x.strip().replace("\n", "").replace("\r", "") for x in content if len(x.strip()) > 3]
        print(content)
        # print(content)
        # 进行数据拆分并创建数据库中的字段数据
        content_len = 0
        for i in range(len(content)):
            txt = content[i]
            index = int(i + 1)
            img = os.path.join(type_path, en_name, "data_png", str(index) + ".png")
            task = TaskEach.objects.filter(txt=txt, task_id=task_id).first()
            if task:
                content_len = content_len + 0
            else:
                TaskEach.objects.update_or_create(
                    txt=txt,
                    index=index,
                    img=img,
                    task_id=task_id,
                    prompt="待处理",
                    ts="待处理"
                )
                content_len = content_len + 1
        content_len_txt = "没有可以拆分的数据" if content_len == 0 else "拆分条目数：{}".format(content_len)

        # 创建需要的文件夹
        path_image = os.path.join(BASE_DIR, "Txt2Video", type_path)
        if not os.path.exists(path_image):
            os.mkdir(path_image)
        # 创建每个项目
        path_en_name = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name)
        if not os.path.exists(path_en_name):
            os.mkdir(path_en_name)
        # 图片保存路径
        path_image = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "data_png")
        if not os.path.exists(path_image):
            os.mkdir(path_image)
        # 音频每个路径
        path_each_audio = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "each_audio_wav")
        if not os.path.exists(path_each_audio):
            os.mkdir(path_each_audio)
        # 音频合并路径
        path_audio = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "audio_wav")
        if not os.path.exists(path_audio):
            os.mkdir(path_audio)
        # 数据结果路径
        path_result = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "data_result")
        if not os.path.exists(path_result):
            os.mkdir(path_result)

        print_info = [
            "文章拆分完毕",
            content_len_txt,
            "文章类别：{}".format(data.type),
            "英文名称：{}".format(data.en_name),
            "中文名称：{}".format(data.cn_name),
        ]

        print_with_border(print_info)

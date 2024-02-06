# -*- coding: UTF-8 -*-
import wave
from NovelAIUser.settings import *
from Data.models import *
from Config.models import *

try:
    from apps.Utils.script.GeneralTools import *
except:
    from apps.Utils.pyd.GeneralTools import *
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


def step_2_process(num, Task, TaskEach):
    # 用户数据验证
    result_info = user_authenticate()
    print(result_info["msg"])

    if '用户验证通过' in result_info["msg"]:
        ##### 稿件拆分部分 #####
        step_1_function(num, Task, TaskEach)
        ##### GPT关键词生成 #####
        step_2_function(num, Task, TaskEach)
        ##### TTS语音生成 #####
        step_3_function(num, Task, TaskEach)
        ##### SD绘画 #####
        step_4_function(num, Task, TaskEach)
        ##### 剪映配置文件 #####
        step_3_process(num, Task, TaskEach)

# -*- coding: UTF-8 -*-
from datetime import datetime
from moviepy.editor import *
from random import choice
import requests
import hashlib
import platform
import uuid
import json
from NovelAIUser.settings import *


# 机器识别，唯一绑定，利用本机的MAC加密后操作。
def generate_unique_identifier():
    # 获取计算机名称
    computer_name = platform.node()
    # 获取处理器信息
    processor_name = platform.processor()
    # 获取 MAC 地址
    mac_address = ':'.join(hex(uuid.getnode())[2:].zfill(12)[i:i + 2] for i in range(0, 12, 2))
    # 组合机器信息
    machine_info = f'{computer_name}-{processor_name}-{mac_address}'
    # 使用哈希算法生成唯一标识符
    unique_identifier = hashlib.sha256(machine_info.encode()).hexdigest()
    return unique_identifier


# 用户网络验证环节
def user_authenticate(UserData):
    UserData['unique_identifier'] = generate_unique_identifier()
    UserData['part_name'] = 'txt2video/base1'
    # 定义请求的 URL
    url = 'http://url/User/UserManagerView/'
    # 发送 POST 请求
    response = requests.post(url, data=UserData)
    # 解析响应
    if response.status_code == 200:
        result = json.loads(response.text)
        return result
    else:
        return "验证未通过，请联系管理员"


def get_duration(row):
    # 将字符串类型的时间转换为datetime类型的时间
    start_datetime = datetime.strptime(row['start_time_'], '%H:%M:%S')
    end_datetime = datetime.strptime(row['end_time_'], '%H:%M:%S')
    # 计算时间差得到持续时间
    duration = (end_datetime - start_datetime).total_seconds()
    return duration


def get_second(time_str):
    # 使用split()函数分割时间字符串
    hour, minute, second = time_str.split(':')
    # 将分割后的字符串转换为整型
    hour = int(hour)
    minute = int(minute)
    second = int(second)
    # 计算总秒数
    total_seconds = hour * 3600 + minute * 60 + second
    return total_seconds


# 图片移动方法 定义图片的移动方式
# 纵向图片向上移动  'center','top'
def VerticalImageUp(image_speed, sd_image_height):
    fl = lambda gf, t: gf(t)[int(image_speed * t):int(image_speed * t) + int(sd_image_height * 1.8), :]
    return fl, ('center', 'center')


# 纵向图片向左移动  'center','top'
def VerticalImageLeft(image_speed, sd_image_height):
    fl = lambda gf, t: gf(t)[:, int(image_speed * t):int(image_speed * t) + int(sd_image_height * 1.8)]
    return fl, ('center', 'center')


# 横向图片向上移动  'center','top'
def HorizontalUp(image_speed, sd_image_height):
    fl = lambda gf, t: gf(t)[int(image_speed * t):int(image_speed * t) + int(sd_image_height * 0.7), :]
    return fl, ('center', 'top')


# 横向图片向左移动  'center','top'
def HorizontalLeft(image_speed, sd_image_height):
    fl = lambda gf, t: gf(t)[:, int(image_speed * t):int(image_speed * t) + int(sd_image_height * 1.8)]
    return fl, ('center', 'top')


def process_menu_number(num, data_list, sd_json, en_name, type_path, project_title):
    sd_image_width = sd_json['sd_image_width']
    sd_image_height = sd_json['sd_image_height']
    moviepy_factor = sd_json['moviepy_factor']
    video_format = sd_json['video_format']
    image_speed = sd_json['image_speed']

    sd_image_width = sd_image_width * moviepy_factor  # 图片宽度，同样也是视频的宽度
    sd_image_height = sd_image_height * moviepy_factor  # 图片高度，同样也是视频的高度

    # 定义项目导出路径
    project_path = os.path.join(MediaDir, type_path, en_name, "data_result")
    # 如果目标目录不存在则创建
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    # 定义音频素材路径
    each_path_mp3 = os.path.join(MediaDir, type_path, en_name, "each_audio_wav")
    path_mp3 = os.path.join(MediaDir, type_path, en_name, "audio_wav")
    # 定音图片素材路径
    path_png = os.path.join(MediaDir, type_path, en_name, "data_png")

    # print(data_list)
    # 设置集合顺序
    data_list = [i.index for i in data_list]
    print(data_list)

    # 创建图片素材集合
    clips = []
    # 设置音频，视频起始时间
    time_start = 0
    for n in data_list:
        #     print(time_start)
        # 获取音频的时长做为duration
        audio_path = os.path.join(each_path_mp3, str(n) + ".wav")
        audio_file = AudioFileClip(audio_path)
        audio_duration = audio_file.duration
        # 设置音频，视频持续时间
        time_duration = audio_duration
        # 获取素材图片
        img_path = os.path.join(path_png, str(n) + ".png")
        #     print(audio_path,img_path)
        #     print(time_duration)

        clip_image = (
            ImageClip(img_path).set_start(time_start).set_duration(time_duration).resize(
                (sd_image_width, sd_image_height))
        )

        if video_format == 'h':
            # 图片移动方法
            fl, set_pos = choice([
                VerticalImageUp(image_speed, sd_image_height),  # 纵向图片向下移动
                VerticalImageLeft(image_speed, sd_image_height)  # 纵向图片向右移动
            ])
        elif video_format == 'w':
            # 图片移动方法
            fl, set_pos = choice([
                HorizontalUp(image_speed, sd_image_height),  # 横向图片向上移动
                HorizontalLeft(image_speed, sd_image_height),  # 横向图片向左移动
            ])

        moving_image = clip_image.fl(fl, apply_to=['mask'])
        clips.append(moving_image.set_pos(set_pos))

        time_start = time_start + time_duration
    #     print(time_start)

    # 载入背景视频
    path = os.path.join(BASE_DIR, "materials_base", "base.mp4")
    # 计算全部mp3音频的时长
    audio_file_path = os.path.join(path_mp3, en_name + ".wav")
    audio_file = AudioFileClip(audio_file_path)
    # 计算音频的时长
    audio_duration = audio_file.duration
    # print(audio_duration)
    # 创建视频背景设置视频长度
    video = VideoFileClip(path).resize((int(sd_image_width * 0.7), int(sd_image_height * 0.7))).set_duration(
        audio_duration)
    # 拼接素材片段
    final_clip = concatenate_videoclips(clips)
    final_clip_duration = final_clip.duration
    # 计算加速倍数
    speed_ratio = final_clip_duration / audio_duration
    # print(speed_ratio)
    audio_file = audio_file
    # 合并视频和素材片段
    cvc = CompositeVideoClip([video] + clips, size=(int(sd_image_width * 0.7), int(sd_image_height * 0.7))).speedx(
        speed_ratio)
    cvc = cvc.set_audio(audio_file).set_duration(audio_duration)

    video_path = os.path.join(project_path, project_title + ".mp4")
    cvc.write_videofile(video_path, fps=30)


def step_5_fuction(num, UserData, Task, TaskEach):
    try:
        del UserData['tts_num']
        del UserData['content']
    except:
        pass
    result_info = user_authenticate(UserData)
    print(result_info["msg"])

    # 获取SD相关的参数
    u = UserData["username"]
    p = UserData["password"]
    i = generate_unique_identifier()
    sd_url = "http://url/Setting/StableDiffusionView/?u={}&p={}&i={}".format(u, p, i)
    html = requests.get(sd_url).text
    sd_json = json.loads(html)['setting_data']
    # print(sd_json)

    if '用户验证通过' in result_info["msg"]:
        data = Task.objects.filter(id=num).first()
        project_title = data.cn_name
        en_name = data.en_name
        type_path = data.type
        task_id = data.id
        print(project_title, en_name, type_path, task_id)

        # print(task_id)
        data_list = TaskEach.objects.filter(task_id=task_id)

        process_menu_number(num, data_list, sd_json, en_name, type_path, project_title)

    # # 读取表单
    # df = pd.read_excel("task_menu/task.xlsx", skiprows=1)
    # # 筛选未完成的故事行
    # df = df[df["status"] == "未完成"]
    # df.reset_index(drop=True, inplace=True)
    # # process_menu_number(0, df)
    # # 每次生成一个视频
    # for num in range(len(df)):
    #     process_menu_number(num, df)

    # print("脚本执行结束")

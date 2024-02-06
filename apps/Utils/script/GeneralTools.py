# -*- coding: UTF-8 -*-
import platform
import uuid
import hashlib
import requests
import json
from pydub import AudioSegment
from Config.models import *

base_url = ""
# base_url = "http://192.168.110.234"


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


# 用户注册
def registration(user_name):
    url = base_url + '/User/Registration/'
    UserData = {
        "user_name": user_name,
        "identifier": generate_unique_identifier()
    }
    # 发送 POST 请求
    response_str = requests.post(url, data=UserData)
    # 解码JSON响应字符串
    # print(response_str)
    response_dict = json.loads(response_str.text)
    # 提取信息并解码Unicode字符
    message = response_dict['msg']
    # print(message)
    return message


# 用户网络验证环节
def user_authenticate():
    user_info = UserInfo.objects.first()
    username = user_info.username
    password = user_info.password
    UserData = {
        'username': username,
        'password': password,
        # 'unique_identifier': generate_unique_identifier(),
        # 'part_name': 'PaidProject'
    }

    # 定义请求的 URL
    url = base_url + '/User/UserManagerView/'
    # 发送 POST 请求
    response = requests.post(url, data=UserData)
    # 解析响应
    result = json.loads(response.text)
    return result


# 输出格式美化
def print_with_border(print_info):
    # 获取最长行的长度
    max_length = max([len(info) for info in print_info])
    print('*' * (max_length + 4 * 2))
    for info in print_info:
        print('* {0:<{1}} *'.format(info, max_length))
    print('*' * (max_length + 4 * 2))


# 提交语音字数到服务器
def post_point(use_type, data):
    user_info = UserInfo.objects.first()

    username = user_info.username
    password = user_info.password
    UserData = {
        'username': username,
        'use_type': use_type,
        'data': data,
    }

    # 定义请求的 URL
    url = base_url + '/Data/UsePoint/'
    # 发送 POST 请求
    response = requests.post(url, data=UserData)


# 判断额度是否充足
def get_point():
    user_info = UserInfo.objects.first()
    username = user_info.username
    password = user_info.password
    url = base_url + '/Setting/PointJudge/?u={}&p={}'.format(username, password)
    response = requests.get(url)
    result = json.loads(response.text)
    return result


# 判断TTS状态
def get_tts_status():
    user_info = UserInfo.objects.first()
    username = user_info.username
    password = user_info.password
    url = base_url + '/Setting/TTSJudge/?u={}&p={}'.format(username, password)
    response = requests.get(url)
    result = json.loads(response.text)
    return result


# 切掉音频无声方法
def remove_silence(audio, silence_threshold=-80.0, chunk_size=10):
    non_silent_chunks = [chunk for chunk in audio if chunk.dBFS > silence_threshold]
    if len(non_silent_chunks) > 0:
        audio_without_silence = non_silent_chunks[0]
        for chunk in non_silent_chunks[1:]:
            audio_without_silence += chunk
        return audio_without_silence
    else:
        return AudioSegment.silent(duration=len(audio))


# 获取ChatGPT数据配置
def get_chat_gpt_model():
    chat_gpt = ChatGPT.objects.last()
    chat_gpt = chat_gpt.__dict__
    del chat_gpt["_state"]
    del chat_gpt["id"]
    return chat_gpt


# 获取Stable Diffusion数据配置
def get_stable_diffusion_model():
    get_stable_diffusion = StableDiffusion.objects.last()
    get_stable_diffusion = get_stable_diffusion.__dict__
    del get_stable_diffusion["_state"]
    del get_stable_diffusion["id"]
    return get_stable_diffusion


# 获取微软TTS配置
def get_TTS_model():
    get_tts = TTS_MICROSOFT.objects.last()
    get_tts = get_tts.__dict__
    del get_tts["_state"]
    del get_tts["id"]
    return get_tts


# 获取剪映配置
def get_JY_model():
    get_jianying = JianYing.objects.last()
    get_jianying = get_jianying.__dict__
    del get_jianying["_state"]
    del get_jianying["id"]
    return get_jianying

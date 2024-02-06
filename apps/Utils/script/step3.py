# -*- coding: UTF-8 -*-
import http.client
from xml.etree import ElementTree
import wave
import os
from moviepy.editor import *
import re
from Config.models import *
from NovelAIUser.settings import *
from pydub import AudioSegment
from moviepy.audio.fx import audio_fadein, audio_fadeout

try:
    from apps.Utils.script.GeneralTools import *
except:
    from apps.Utils.pyd.GeneralTools import *


# Note: new unified SpeechService API key and issue token uri is per region
# New unified SpeechService key
# Free: https://azure.microsoft.com/en-us/try/cognitive-services/?api=speech-services
# Paid: https://go.microsoft.com/fwlink/?LinkId=872236
# 后台地址：https://portal.azure.com/#home

# TTS生成关键词方法
def TTS_make_2(tts_json, tts_status, audio_path, text, tts_used_info, prompt):
    params = ""
    gender = tts_json["speech_gender"]
    style = tts_json["speech_style"]
    name = tts_json["speech_name"]
    audio_rate = str(tts_json["audio_rate"])
    # 判断是否拥有过API
    if tts_status == "公用":
        TTS_apiKey = tts_used_info["key"]
        print("使用购买的API开始生成文本")
    else:
        TTS_apiKey = TTS_MICROSOFT.objects.first().api_key
        print("使用自己的API开始生成文本")
        print("如果此路径下无法生成音频文件，请检查config文件下TTS.py的API是否有效。")
        print(audio_path + ".wav")

    headers = {"Ocp-Apim-Subscription-Key": TTS_apiKey}
    # AccessTokenUri = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken";
    path = "/sts/v1.0/issueToken"
    print("正在连接微软服务器以获取文本转语音访问令牌")
    conn = http.client.HTTPSConnection(tts_json["access_token_host"])
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    # print(response.status, response.reason)
    if response.status == 200:
        print("微软API身份验证成功")
    else:
        print("微软身份验证失败\n请检查config/authenticate.py文件中【微软TTS APIkey】是否有效")
        print("如果使用购买的API请在config/authenticate.py设置apiKey == \"\"")
    data = response.read()
    conn.close()
    accesstoken = data.decode("UTF-8")
    # print("Access Token: " + accesstoken)
    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-CN')
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-CN')
    voice.set('{http://www.w3.org/XML/1998/namespace}style', '{}'.format(style))
    voice.set('{http://www.w3.org/XML/1998/namespace}gender', '{}'.format(gender))
    voice.set('name', 'Microsoft Server Speech Text to Speech Voice ({})'.format(name))
    voice.set('rate', audio_rate)
    # 'Microsoft Server Speech Text to Speech Voice (zh-CN, YunxiNeural)'
    print('使用的声音是：{}，风格是：{}，性别是：{})'.format(name, style, gender))
    voice.text = text
    headers = {"Content-type": "application/ssml+xml",
               "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
               "Authorization": "Bearer " + accesstoken,
               "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
               "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
               "User-Agent": "TTSForPython"}
    # Connect to server to synthesize the wave
    print("连接到服务器以合成音频")
    conn = http.client.HTTPSConnection("eastus.tts.speech.microsoft.com")
    conn.request("POST", "/cognitiveservices/v1", ElementTree.tostring(body), headers)
    response = conn.getresponse()
    # print(response.status, response.reason)
    # 上传数据
    post_point('TTS', text)

    if response.status == 200:
        # 保存音频文件
        data = response.read()
        conn.close()
        # print("验证音频文件波长为: %d" % (len(data)))
        # print(audio_path + ".wav")
        f = wave.open(audio_path + ".wav", "wb")
        f.setnchannels(1)  # 单声道
        f.setframerate(24000)  # 采样率
        f.setsampwidth(2)  # sample width 2 bytes(16 bits)
        f.writeframes(data)
        f.close()

        audio = AudioSegment.from_wav(audio_path + ".wav", )
        audio_without_silence = remove_silence(audio)
        audio_without_silence.export(audio_path + ".wav", format="wav")

        # print("字幕：【{}】，音频文件生成成功。\n文件保存位置：{}".format(text, audio_path + ".wav"))
        # 验证音频文件
        try:
            AudioFileClip(audio_path + ".wav")
            print("验证音频通过，文件为 {}".format(audio_path + ".wav"))
        except:
            print("验证音频失败，文件为 {}".format(audio_path + ".wav"))
            print("正在重新生成音频，{}".format(audio_path + ".wav"))
            # TTS_make_2(result_info, audio_path, text, tts_used_info, prompt)
            TTS_make_2(tts_json, tts_status, audio_path, text, tts_used_info, prompt)
        print("字幕：【{}】，音频文件生成成功。\n文件保存位置：{}".format(text, audio_path + ".wav"))
    else:
        print("字幕：【{}】，音频文件生成失败，尝试重新生成")
        # TTS_make_2(result_info, audio_path, text, tts_used_info, prompt)
        TTS_make_2(tts_json, tts_status, audio_path, text, tts_used_info, prompt)
    print("-" * 50)


def step_3_function(num, Task, TaskEach):
    # 用户数据验证
    result_info = user_authenticate()
    print(result_info["msg"])

    # 获取微软TTS配置
    tts_json = get_TTS_model()

    if '用户验证通过' in result_info["msg"]:
        data_list = Task.objects.filter(id=num)

        # 判断TTS状态
        tts_status = '公用' if get_tts_status()["message"] == 'TTS Status Public' else '自用'
        tts_used_info = get_tts_status()

        if tts_status == '公用':
            audio_len = 0
            for data in data_list:
                cn_name = data.cn_name
                en_name = data.en_name
                type_path = data.type
                task_id = data.id

                # 获取这个任务id所有的任务列表
                path_each_audio = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "each_audio_wav")
                path_audio = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "audio_wav")
                txt_list = TaskEach.objects.filter(task_id=task_id)
                for each in txt_list:
                    text = each.txt
                    index = each.index
                    prompt = each.prompt
                    # 判断额度是否充足
                    point_status = get_point()['message']
                    if point_status == "会员积分充足":
                        # 创建音频目录
                        if not os.path.exists(path_each_audio):
                            os.makedirs(path_each_audio)
                        audio_path = os.path.join(path_each_audio, str(index))
                        # 如果音频文件存在则跳过
                        audio_path = os.path.join(audio_path)
                        if os.path.exists(audio_path + ".wav"):
                            pass
                        else:
                            TTS_make_2(tts_json, tts_status, audio_path, text, tts_used_info, prompt)
                            audio_len = audio_len + 1
                    else:
                        print('会员积分不足，请联系管理员')
                        break

                # 拼接音频
                wav_list = os.listdir(path_each_audio)
                sorted_filenames = sorted(wav_list, key=lambda x: int(re.search(r'\d+', x).group()))
                # print(sorted_filenames)
                audio_clips = []
                for filename in sorted_filenames:
                    filepath = os.path.join(path_each_audio, filename)
                    # print(filepath)
                    audio_clip = AudioFileClip(filepath)
                    audio_clip = audio_clip.audio_fadein(0.5)
                    audio_clips.append(audio_clip)

                final_clip = concatenate_audioclips(audio_clips)
                if not os.path.exists(path_audio):
                    os.makedirs(path_audio)
                audio_file_path = os.path.join(path_audio, en_name + ".wav")
                final_clip.write_audiofile(audio_file_path)  # 保存拼接后的音频文件
                print(tts_used_info['message'])

        elif tts_status == '自用':
            audio_len = 0
            for data in data_list:
                cn_name = data.cn_name
                en_name = data.en_name
                type_path = data.type
                task_id = data.id

                # 获取这个任务id所有的任务列表
                path_each_audio = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "each_audio_wav")
                path_audio = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "audio_wav")
                txt_list = TaskEach.objects.filter(task_id=task_id)
                for each in txt_list:
                    text = each.txt
                    index = each.index
                    prompt = each.prompt

                    if not os.path.exists(path_each_audio):
                        os.makedirs(path_each_audio)
                    audio_path = os.path.join(path_each_audio, str(index))
                    # print(audio_path, text)
                    # 判断如果音频文件存在则跳过
                    audio_path = os.path.join(audio_path)
                    if os.path.exists(audio_path + ".wav"):
                        pass
                    else:
                        TTS_make_2(tts_json, tts_status, audio_path, text, tts_used_info, prompt)
                        audio_len = audio_len + 1

                # 拼接音频
                wav_list = os.listdir(path_each_audio)
                sorted_filenames = sorted(wav_list, key=lambda x: int(re.search(r'\d+', x).group()))
                # print(sorted_filenames)
                audio_clips = []
                for filename in sorted_filenames:
                    filepath = os.path.join(path_each_audio, filename)
                    # print(filepath)
                    audio_clip = AudioFileClip(filepath)
                    audio_clip = audio_clip.audio_fadein(0.5)
                    audio_clips.append(audio_clip)

                final_clip = concatenate_audioclips(audio_clips)
                if not os.path.exists(path_audio):
                    os.makedirs(path_audio)
                audio_file_path = os.path.join(path_audio, en_name + ".wav")
                final_clip.write_audiofile(audio_file_path)  # 保存拼接后的音频文件
                print('记得每个月去TTS后台更新服务，否则无法继续使用哟~')

        audio_len_txt = "音频无需生成" if audio_len == 0 else "生成音频条目数：{}".format(audio_len)

        print_info = [
            "生成分段音频以及合成完毕",
            audio_len_txt,
            "文章类别：{}".format(data.type),
            "英文名称：{}".format(data.en_name),
            "中文名称：{}".format(data.cn_name),
        ]

        print_with_border(print_info)

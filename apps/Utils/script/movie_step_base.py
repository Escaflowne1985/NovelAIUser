# -*- coding: UTF-8 -*-
from Data2.models import *
from Config.models import *
from NovelAIUser.settings import *
import os
import requests
import hashlib
import platform
import uuid
import json
from NovelAIUser.settings import *

try:
    from apps.Utils.script.step2 import *
except:
    from apps.Utils.pyd.step2 import *
try:
    from apps.Utils.script.step3 import *
except:
    from apps.Utils.pyd.step3 import *
try:
    from apps.Utils.script.GeneralTools import *
except:
    from apps.Utils.pyd.GeneralTools import *


# 时间转换函数 时间转换成秒数
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


# 数据拼接拆分
def get_srt_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt):
    # 知数云API
    if 'zhishuyun.com' in api_url:
        url = api_url + api_key
        # print(question_txt_1 + txt_each + question_txt_2)
        payload = {'question': questions_gpt['question_txt_1'] + txt_each + questions_gpt['question_txt_2']}
        response = post_with_retry_zhishuyun(url, payload, max_retries, retry_time)
        text = json.loads(response.text)["answer"]
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：", text)

    # openAI
    if "openai.com" in api_url:
        # print(openai)
        text = post_with_retry_gpt35(api_key, questions_gpt, txt_each, max_retries)
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：{}".format(text))

    # CloseAI
    if "api.closeai-proxy.xyz" in api_url:
        # print(closeai)
        text = post_with_retry_CloseAI(api_key, questions_gpt, txt_each, max_retries)
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：", text)

    # ClaudeAI【free】
    if "claude.ai" in api_url:
        # print(closeai)
        text = post_with_retry_ClaudeAI_Free(questions_gpt, txt_each, max_retries)
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：", text)

    # ClaudeAI【pay】
    if "api.anthropic.com" in api_url:
        # print(closeai)
        text = post_with_retry_ClaudeAI_Pay(questions_gpt, txt_each, max_retries)
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：", text)

    # 百度直译【Free】
    if "fanyi.baidu.com" in api_url:
        text = ts.translate_text(txt_each, to_language='en')
        text = ts.translate_text(text, to_language='cn')
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述直接翻译结果：", text)

    print("原文内容：【{}】".format(txt_each))
    print("改写结果：{}".format(text))
    print("-" * 50)
    return text


# 依据GPT处理关键词
def process_menu_number(txt_new_list, api_url, api_key, max_retries, retry_time, questions_gpt, MovieTaskEach):
    for each in txt_new_list:
        txt_each = each.txt
        id_ = each.id
        text = get_srt_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt)
        MovieTaskEach.objects.filter(id=id_).update(txt_new=text)
        time.sleep(0.5)


# 生成字幕
def make_whisper(request, num):
    result_info = user_authenticate()
    print(result_info["msg"])

    if '用户验证通过' in result_info["msg"]:
        # 获取模型保存的路径
        whisper_model_path = os.path.join(BASE_DIR, "MovieProcess", "models")

        # 获取视频设置基础参数
        last_record = PythonEnv.objects.last()
        # 使用values()方法将模型实例转换为字典
        last_record_dict = last_record.__dict__
        # 删除不必要的键 '_state'，它不是模型字段
        del last_record_dict['_state'], last_record_dict['id']
        python_env_path = last_record_dict['python_env_path']
        whisper_model = last_record_dict['whisper_model']

        # 稿件拆分部分
        task_id = MovieTask.objects.filter(id=num).first().id
        type_path = MovieTask.objects.filter(id=num).first().type
        en_name = MovieTask.objects.filter(id=num).first().en_name

        # 创建项目路径文件夹,结果文件也会保存到这下面
        movie_project_dir = os.path.join(BASE_DIR, "MovieProcess", "result", type_path)
        if not os.path.exists(movie_project_dir):
            os.mkdir(movie_project_dir)
        movie_project_dir = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name)
        if not os.path.exists(movie_project_dir):
            os.mkdir(movie_project_dir)
        # 创建字幕保存文件夹
        movie_project_srt = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, 'srt')
        if not os.path.exists(movie_project_srt):
            os.mkdir(movie_project_srt)
        # 创建逐段音频文件夹
        movie_project_audio_each = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, 'each_audio_wav')
        if not os.path.exists(movie_project_audio_each):
            os.mkdir(movie_project_audio_each)
        # 创建整合好的音频文件夹
        movie_project_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, 'each_audio')
        if not os.path.exists(movie_project_audio):
            os.mkdir(movie_project_audio)
        # 读取源文件的mp4，并提取字幕
        video_path = os.path.join(BASE_DIR, "MovieProcess", "base", en_name + ".mp4")
        # 执行cmd命令提取字幕
        whisper_exe_path = os.path.join(python_env_path, 'Scripts', 'whisper.exe')
        python_exe_path = os.path.join(python_env_path, 'python.exe')
        cmd = "{} {} {} --output_dir {} --language Chinese --model_dir {} --model {}".format(
            python_exe_path, whisper_exe_path, video_path, movie_project_srt, whisper_model_path, whisper_model)
        os.system(cmd)

        print(en_name, "字幕提取执行结束")

    # 读取字幕文件写入ORM
    movie_project_srt_file = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, 'srt', en_name + ".srt")
    # 使用re模块定义正则表达式
    pattern = r'(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\n(.*)\n\n'
    # 读取srt文件，并使用正则表达式提取时间和字幕
    with open(movie_project_srt_file, 'r', encoding="utf8") as f:
        srt_data = f.read()
        subtitle_list = re.findall(pattern, srt_data)

    # 进行数据拆分并创建数据库中的字段数据
    content_len = 0
    for data in subtitle_list:
        txt = data[2]
        start_time = data[0]
        end_time = data[1]
        index = int(content_len + 1)

        task = MovieTaskEach.objects.filter(txt=txt, task_id=task_id).first()
        if task:
            pass
        else:
            MovieTaskEach.objects.update_or_create(
                txt=txt,
                start_time=start_time,
                end_time=end_time,
                task_id=task_id,
                index=index,
                txt_new="待处理"
            )
            content_len += 1


# 内容改写
def movie_srt_all_function(num, MovieTask, MovieTaskEach):
    result_info = user_authenticate()
    print(result_info["msg"])

    if '用户验证通过' in result_info["msg"]:
        # 获取用户gpt配置信息
        u = str(UserData["username"])
        p = str(UserData["password"])
        i = generate_unique_identifier()
        gpt_url = "http://url/Setting/ChatGPT35View/?u={}&p={}&i={}".format(u, p, i)
        html = requests.get(gpt_url).text
        gpt_json = json.loads(html)['setting_data']
        # print(gpt_json)
        api_url = gpt_json['api_url']
        # print(api_url)

        if "zhishuyun.com" in api_url:
            api_key_list = list(GPT_ZSY.objects.values_list('api_key', flat=True))
        elif "openai.com" in api_url:
            api_key_list = list(GPT_OPENAI.objects.values_list('api_key', flat=True))
        elif "api.closeai-proxy.xyz" in api_url:
            api_key_list = list(GPT_CLOSEAI.objects.values_list('api_key', flat=True))

        # api_key = gpt_json['api_key']
        max_retries = gpt_json['max_retries']
        retry_time = None if gpt_json['retry_time'] == 0 else gpt_json['retry_time']
        questions_gpt = questions_gpt_dict[gpt_json['questions_gpt']]
        # print(questions_gpt)

        # 判断是否是自定义关键词
        if gpt_json["questions_gpt"] == "自定义组合":
            questions_gpt["question_txt_1"] = gpt_json["questions_txt_1"]
            questions_gpt["question_txt_2"] = gpt_json["questions_txt_2"]

        data_list = MovieTask.objects.filter(id=num)

        print("使用openai的用户验证成功请抓紧切换代理")
        print("这里设置了3秒延迟，任务在3秒后开启")
        time.sleep(3)

        for data in data_list:
            cn_name = data.cn_name
            en_name = data.en_name
            type_path = data.type
            task_id = data.id

            # 获取这个任务id所有的任务列表
            txt_list = MovieTaskEach.objects.filter(Q(task_id=task_id) & Q(txt_new='待处理'))

            if "openai.com" in api_url:
                # 获取 openai-key 列表
                openai_key_list = api_key_list
                openai_key_len = len(openai_key_list)
                # 拆分任务列表
                # print(openai_key_len, openai_key_list)
                # print(len(txt_list))
                data_list = split_list(txt_list, openai_key_len)
                print("还要处理的数据条数：", len(txt_list))
                print("如果openai-key设置多个，开启多线程处理")
                for n in range(len(openai_key_list)):
                    api_key = openai_key_list[n]
                    txt_new_list = data_list[n]
                    thread = threading.Thread(target=process_menu_number, args=(
                        txt_new_list, api_url, api_key, max_retries, retry_time, questions_gpt, MovieTaskEach))
                    thread.start()

            elif "zhishuyun.com" in api_url:
                # print(txt_list)
                api_key = api_key_list[0]
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    text = get_srt_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt)
                    MovieTaskEach.objects.filter(id=id_).update(txt_new=text)
                    time.sleep(0.5)

            elif "api.closeai-proxy.xyz" in api_url:
                # 获取 openai-key 列表
                close_key_list = api_key_list
                close_key_len = len(close_key_list)
                # 拆分任务列表
                # print(openai_key_len, openai_key_list)
                # print(len(txt_list))
                data_list = split_list(txt_list, close_key_len)
                print("还要处理的数据条数：", len(txt_list))
                print("如果openai-key设置多个，开启多线程处理")
                for n in range(len(close_key_list)):
                    api_key = close_key_list[n]
                    txt_new_list = data_list[n]
                    thread = threading.Thread(target=process_menu_number, args=(
                        txt_new_list, api_url, api_key, max_retries, retry_time, questions_gpt, MovieTaskEach))
                    thread.start()

            elif "claude.ai" in api_url:
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    api_key = ""
                    text = get_srt_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt)
                    MovieTaskEach.objects.filter(id=id_).update(txt_new=text)
                    time.sleep(0.5)

            elif "api.anthropic.com" in api_url:
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    api_key = ""
                    text = get_srt_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt)
                    MovieTaskEach.objects.filter(id=id_).update(txt_new=text)
                    time.sleep(0.5)


# 音频生成
def movie_audio_function(num, MovieTask, MovieTaskEach):
    result_info = user_authenticate()
    print(result_info["msg"])
    # 获取微软TTS配置
    tts_json = get_TTS_model()

    if '用户验证通过' in result_info["msg"]:
        # 判断TTS状态
        tts_status = '公用' if get_tts_status()["message"] == 'TTS Status Public' else '自用'
        tts_used_info = get_tts_status()

        data_list = MovieTask.objects.filter(id=num)

        if tts_status == '公用':
            audio_len = 0
            for data in data_list:
                cn_name = data.cn_name
                en_name = data.en_name
                type_path = data.type
                task_id = data.id

                # 获取这个任务id所有的任务列表
                path_each_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "each_audio_wav")
                path_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "audio_wav")
                txt_list = MovieTaskEach.objects.filter(task_id=task_id)
                for each in txt_list:
                    text = each.txt_new
                    index = each.index
                    prompt = ""
                    # 判断额度是否充足
                    point_status = get_point()['message']
                    if point_status == "会员积分充足":
                        # 创建每一段音频的目录
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


        elif tts_status == '自用':
            audio_len = 0
            for data in data_list:
                cn_name = data.cn_name
                en_name = data.en_name
                type_path = data.type
                task_id = data.id

                # 获取这个任务id所有的任务列表
                path_each_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "each_audio_wav")
                path_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "audio_wav")
                txt_list = MovieTaskEach.objects.filter(task_id=task_id)
                for each in txt_list:
                    text = each.txt_new
                    index = each.index
                    prompt = ""

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


# 音频合并保存成最后结果
def movie_merge_function(num):
    result_info = user_authenticate()
    print(result_info["msg"])

    if '用户验证通过' in result_info["msg"]:
        data_list = MovieTask.objects.filter(id=num).first()
        type_path = data_list.type
        en_name = data_list.en_name
        cn_name = data_list.cn_name

        # 获取音频时长
        base_video_path = os.path.join(BASE_DIR, "MovieProcess", "base", en_name + ".mp4")
        input_audio_path = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "audio_wav", en_name + ".wav")
        output_path = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, cn_name + ".mp4")
        # 加载视频和音频
        video_clip = VideoFileClip(base_video_path)
        audio_clip = AudioFileClip(input_audio_path)
        # 获取视频时长
        video_duration = video_clip.duration
        # 根据视频时长对音频进行加速或减速
        new_audio_clip = audio_clip.fx(lambda x: x.set_duration(video_duration))
        # 保存新的音频文件
        new_audio_path = "new_audio.mp3"
        new_audio_clip.write_audiofile(new_audio_path)
        ffmpeg_command = f"ffmpeg -y -i {base_video_path} -i {new_audio_path} -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 {output_path}"
        print(ffmpeg_command)
        os.system(ffmpeg_command)
        # 删除新的音频文件
        os.remove(new_audio_path)


# 保存处理单条音频
def movie_audio_each_save_function(num, index):
    result_info = user_authenticate()
    print(result_info["msg"])

    if '用户验证通过' in result_info["msg"]:
        data_list = MovieTask.objects.filter(id=num).first()
        type_path = data_list.type
        en_name = data_list.en_name

        # 删除制定wav文件
        del_wav_path = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "each_audio_wav", str(index) + ".wav")
        try:
            os.remove(del_wav_path)
        except:
            pass

        # 获取微软TTS配置
        tts_json = get_TTS_model()
        # 判断TTS状态
        tts_status = '公用' if get_tts_status()["message"] == 'TTS Status Public' else '自用'
        tts_used_info = get_tts_status()

        data_list = MovieTask.objects.filter(id=num)

        if tts_status == '公用':
            audio_len = 0
            for data in data_list:
                cn_name = data.cn_name
                en_name = data.en_name
                type_path = data.type
                task_id = data.id

                # 获取这个任务id所有的任务列表
                path_each_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "each_audio_wav")
                path_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "audio_wav")
                txt_list = MovieTaskEach.objects.filter(task_id=task_id, index=index)
                for each in txt_list:
                    text = each.txt
                    index = each.index
                    prompt = ""
                    # 判断额度是否充足
                    point_status = get_point()['message']
                    if point_status == "会员积分充足":
                        # 创建每一段音频的目录
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
                path_each_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "each_audio_wav")
                path_audio = os.path.join(BASE_DIR, "MovieProcess", "result", type_path, en_name, "audio_wav")
                txt_list = MovieTaskEach.objects.filter(task_id=task_id, index=index)
                for each in txt_list:
                    text = each.txt_new
                    index = each.index
                    prompt = ""

                    if not os.path.exists(path_each_audio):
                        os.makedirs(path_each_audio)
                    audio_path = os.path.join(path_each_audio, str(index))
                    # print(audio_path, text)
                    # 判断如果音频文件存在则跳过
                    audio_path = os.path.join(audio_path)
                    if os.path.exists(audio_path + ".wav"):
                        pass
                    else:
                        TTS_make_2(tts_json, tts_status, audio_path, text, tts_used_info, UserData, prompt)
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

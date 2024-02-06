# -*- coding: UTF-8 -*-
import re
import random
from requests.exceptions import RequestException
import time
from django.db.models import Q
import openai
from Config.models import *
from Data.models import *
import threading
import translators as ts

try:
    from apps.Utils.script.GeneralTools import *
except:
    from apps.Utils.pyd.GeneralTools import *

questions_gpt_dict = {
    "自定义组合": {
        "question_txt_1": '',
        "question_txt_2": '\n'
    },
    "关键词描述权重版1": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "关键词描述权重版2": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "关键词描述漫画导演版": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "关键词描述故事叙述版": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "语义切割短句版": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "语义切割长句版": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "都市情景叙述版": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "【电影解说改写】": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
}

questions_gpt_each_dict = {
    "人物描述模式": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "拍摄方法模式": {
        "question_txt_1": '',
        "question_txt_2": ''
    },
    "画面镜头模式": {
        "question_txt_1": '',
        "question_txt_2": ''
    },

}


# GPT 知数云
def post_with_retry_zhishuyun(url, payload, max_retries, retry_time):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=retry_time)
            return response
        except (RequestException, ConnectionError):
            retries += 1
            print(f"【知数云】GPT35生成关键词失败，尝试启动第 {retries}/{max_retries} 次")
            time.sleep(3)
    print(f"重试次数超过 ({max_retries}) 次，你的网太烂了，重来吧")
    return None


# GPT OPENAI
def post_with_retry_gpt35(api_key, questions_gpt, txt_each, max_retries):
    openai.api_key = api_key
    retries = 0
    # time.sleep(1)
    while retries < max_retries:
        try:
            # print("正在生成分镜数据需要的信息")
            # t1 = "请将【】中的内容用丰富的中文描述描绘一副静态画面。【"
            # t2 = "】直接开始给出中文描述不需要其他自然语言描述。"
            # chat_completion = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     request_timeout=100,
            #     messages=[
            #         # system message first, it helps set the behavior of the assistant
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         # I am the user, and this is my prompt
            #         {"role": "user",
            #          "content": t1 + txt_each + t2},
            #         # we can also add the previous conversation
            #         # {"role": "assistant", "content": "Episode III."},
            #     ],
            # )
            # # print(chat_completion)
            # text = chat_completion.choices[0].message.content
            # time.sleep(random.randint(1, 10))
            # # print("分镜场景描述：",text)
            # print("正在生成分镜数据拆解")
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                request_timeout=100,
                messages=[
                    # system message first, it helps set the behavior of the assistant
                    {"role": "system", "content": "You are a helpful assistant."},
                    # I am the user, and this is my prompt
                    {"role": "user",
                     "content": questions_gpt['question_txt_1'] + txt_each + questions_gpt['question_txt_2']},
                    # we can also add the previous conversation
                    # {"role": "assistant", "content": "Episode III."},
                ],
            )
            # print(chat_completion)
            text = chat_completion.choices[0].message.content
            # print(text)
            return text
            time.sleep(random.randint(1, 5))
        except:
            retries += 1
            print(f"【OPENAI】GPT35生成关键词失败，尝试启动第 {retries}/{max_retries} 次")
            time.sleep(random.randint(1, 10))
    print(f"重试次数超过 ({max_retries}) 次，你的网太烂了，重来吧")
    return None


# GPT CloseAI
def post_with_retry_CloseAI(api_key, questions_gpt, txt_each, max_retries):
    openai.api_base = 'https://api.closeai-asia.com/v1'
    openai.api_key = api_key
    retries = 0
    # time.sleep(1)
    while retries < max_retries:
        try:
            # print("正在生成分镜数据需要的信息")
            # t1 = "请将【】中的内容用丰富的中文描述描绘一副静态画面。【"
            # t2 = "】直接开始给出中文描述不需要其他自然语言描述。"
            # chat_completion = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     request_timeout=100,
            #     messages=[
            #         # system message first, it helps set the behavior of the assistant
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         # I am the user, and this is my prompt
            #         {"role": "user",
            #          "content": t1 + txt_each + t2},
            #         # we can also add the previous conversation
            #         # {"role": "assistant", "content": "Episode III."},
            #     ],
            # )
            # # print(chat_completion)
            # text = chat_completion.choices[0].message.content
            # time.sleep(random.randint(1, 10))
            # # print("分镜场景描述：",text)
            # print("正在生成分镜数据拆解")
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                request_timeout=100,
                messages=[
                    # system message first, it helps set the behavior of the assistant
                    {"role": "system", "content": "You are a helpful assistant."},
                    # I am the user, and this is my prompt
                    {"role": "user",
                     "content": questions_gpt['question_txt_1'] + txt_each + questions_gpt['question_txt_2']},
                    # we can also add the previous conversation
                    # {"role": "assistant", "content": "Episode III."},
                ],
            )
            # print(chat_completion)
            text = chat_completion.choices[0].message.content
            # print(text)
            return text
            time.sleep(random.randint(1, 5))
        except:
            retries += 1
            print(f"【CLOSEAI】GPT35生成关键词失败，尝试启动第 {retries}/{max_retries} 次")
            time.sleep(random.randint(1, 10))
    print(f"重试次数超过 ({max_retries}) 次，你的网太烂了，重来吧")
    return None


class FError(Exception):
    pass


# GPT ClaudeAI 【Free】
def post_with_retry_ClaudeAI_Free(questions_gpt, txt_each, max_retries):
    token = ''
    channel = ""

    def send_msg(msg):
        send_url = "https://slack.com/api/chat.postMessage"
        claude = ''

        data = {
            "token": token,
            "channel": channel,
            "text": claude + msg
        }
        response = requests.post(url=send_url, data=data)
        text = json.loads(response.text)
        return text

    def receive_msg(ts):
        send_url = "https://slack.com/api/conversations.history"
        data = {
            "token": token,
            "channel": channel,
            "ts": ts,
            "oldest": ts
        }
        response = requests.post(url=send_url, data=data)
        text = json.loads(response.text)
        # for n in range(len(text['messages'])):
        #     if text['messages'][n]["ts"] == ts:
        #         return text['messages'][n]
        return text

    retries = 0
    while retries < max_retries:
        try:
            txt_each = questions_gpt['question_txt_1'] + txt_each + questions_gpt['question_txt_2']
            data = send_msg(txt_each)
            time.sleep(20)
            ts = data["ts"]
            # print(ts, data)
            text = receive_msg(ts)
            return text["messages"][0]["text"]
        except:
            retries += 1
            print(f"【ClaudeAI_Free】GPT35生成关键词失败，尝试启动第 {retries}/{max_retries} 次")
            time.sleep(random.randint(1, 10))
    print(f"重试次数超过 ({max_retries}) 次，你的网太烂了，重来吧")
    return None


# GPT ClaudeAI 【Pay】
def post_with_retry_ClaudeAI_Pay(questions_gpt, txt_each, max_retries):
    user_info = UserInfo.objects.first()
    username = user_info.username
    password = user_info.password
    url = "http://url/User/UserPrompt1View/"
    # print(username,password)

    retries = 0
    while retries < max_retries:
        try:
            txt_each = questions_gpt['question_txt_1'] + txt_each + questions_gpt['question_txt_2']
            data = {
                "username": username,
                "password": password,
                "question_txt_1": questions_gpt['question_txt_1'],
                "text": txt_each,
                "question_txt_2": questions_gpt['question_txt_2'],
            }
            html = requests.post(url, data=data).text
            js_data = json.loads(html)
            # print(js_data)
            time.sleep(2)
            if js_data["message"] == "没有返回结果请重试":
                return Ferror
            else:
                return js_data["message"]
        except:
            retries += 1
            print(f"【ClaudeAI_Pay】GPT35生成关键词失败，尝试启动第 {retries}/{max_retries} 次")
            time.sleep(random.randint(1, 10))
    print(f"重试次数超过 ({max_retries}) 次，你的网太烂了，重来吧")
    return None


# 百度直译【Free】


# 数据拼接拆分
def get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt, sd_json, lora_dict):
    # 判断每句话中是否有LORA设置的关键信息
    # print(eval(lora_dict))
    text_temp = ""
    try:
        lora_dict = eval(lora_dict)
        key_list = list(lora_dict.keys())  # LoRA配置Key列表
        for key_l in key_list:
            if '@' in key_l:  # 判断包含@符号即有多个配置需要替换
                k_temp_l = key_l.split("@")
                for each_key in k_temp_l:
                    if each_key in txt_each:
                        text_temp = text_temp + lora_dict[key_l]
                        print("提取Lora信息成功，关键词为{}".format(key_l))
            elif '@' not in key_l:
                if key_l in txt_each:
                    text_temp = text_temp + lora_dict[key_l]
                    print("提取Lora信息成功，关键词为{}".format(key_l))
            else:
                print("本句话未匹配到设置的Lora")
    except:
        print("Lora配置不要动，否则出不来结果")

    # 解析配置数据
    prompt = sd_json['prompt']  # SD正面词
    negative = sd_json['negative']  # SD负面词
    # num_max = sd_json['num_max']  # 通用随机最大数
    # print(sd_json)
    # 人物描述
    lora_describe = ""
    # 拍摄方法
    filming_method_str = sd_json['filming_method_str']
    filming_method_num = sd_json['filming_method_num']
    # 画面镜头
    camera_direction_str = sd_json['camera_direction_str']
    camera_direction_num = sd_json['camera_direction_num']

    # 知数云API
    if 'zhishuyun.com' in api_url:
        url = api_url + api_key
        # print(question_txt_1 + txt_each + question_txt_2)
        payload = {'question': questions_gpt['question_txt_1'] + txt_each + questions_gpt['question_txt_2']}
        response = post_with_retry_zhishuyun(url, payload, max_retries, retry_time)
        # print(response.text)
        # 结果样例
        # {
        #     "answer": "以下是一套用于指导AI模型生成描述“而我爸则是舔着脸问我，今天赚了多少钱，够不够家里这个月的生活费”的prompt：\n\n(sad:1.5), (disappointed:1.2), (depressed:1.2), (dark:1.3), (lowkey:1.5), (poor:1.5), (struggling:1.5), (worried:1.5), (serious:1.2), (middle-aged:1.2), (male:1.2), (gray hair:1.2), (wrinkled face:1.2), (frowning:1.2), (dull lighting:1.3), (indoor:1.2), (living room:1.2), (empty room:1.2), (small room:1.2), (bare walls:1.2), (no decorations:1.2), (simple furniture:1.2), (old-fashioned furniture:1.2), (brown furniture:1.2), (noisy background:1.3), (TV sounds:1.3), (money:1.5), (financial stress:1.5), (family pressure:1.5), (monthly expenses:1.5), (not enough:1.5), (struggle to make ends meet:1.5), (hard work:1.5), (sacrifice:1.5), (family responsibility:1.5), (parent-child conflict:1.5)"
        # }
        text = json.loads(response.text)["answer"]
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：", text)
        # 人物描述
        if sd_json["lora_describe_choose"] == "全自动":
            lora_describe_choose_questions_gpt = questions_gpt_each_dict["人物描述模式"]
            lora_describe = post_with_retry_zhishuyun(api_key, lora_describe_choose_questions_gpt, txt_each, max_retries)
            # print("人物描述:", lora_describe)
            print("人物描述自动分析完毕")
        # 拍摄方法
        if sd_json["filming_method_choose"] == "全自动":
            filming_method_choose_questions_gpt = questions_gpt_each_dict["拍摄方法模式"]
            filming_method_str = post_with_retry_zhishuyun(api_key, filming_method_choose_questions_gpt, txt_each, max_retries)
            filming_method_num = sd_json['filming_method_num']
            # print("拍摄方法:", filming_method_str)
            print("拍摄方法自动分析完毕")
        # 画面镜头
        if sd_json["camera_direction_choose"] == "全自动":
            camera_direction_choose_questions_gpt = questions_gpt_each_dict["画面镜头模式"]
            camera_direction_str = post_with_retry_zhishuyun(api_key, camera_direction_choose_questions_gpt, txt_each, max_retries)
            camera_direction_num = sd_json['camera_direction_num']
            # print("画面镜头:", camera_direction_str)
            print("画面镜头自动分析完毕")

    # openAI
    if "openai.com" in api_url:
        # print(openai)
        text = post_with_retry_gpt35(api_key, questions_gpt, txt_each, max_retries)
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：{}".format(text))
        # 人物描述
        if sd_json["lora_describe_choose"] == "全自动":
            lora_describe_choose_questions_gpt = questions_gpt_each_dict["人物描述模式"]
            lora_describe = post_with_retry_gpt35(api_key, lora_describe_choose_questions_gpt, txt_each, max_retries)
            print("人物描述:", lora_describe)
            print("人物描述自动分析完毕")
        # 拍摄方法
        if sd_json["filming_method_choose"] == "全自动":
            filming_method_choose_questions_gpt = questions_gpt_each_dict["拍摄方法模式"]
            filming_method_str = post_with_retry_gpt35(api_key, filming_method_choose_questions_gpt, txt_each, max_retries)
            filming_method_num = sd_json['filming_method_num']
            print("拍摄方法:", filming_method_str)
            print("拍摄方法自动分析完毕")
        # 画面镜头
        if sd_json["camera_direction_choose"] == "全自动":
            camera_direction_choose_questions_gpt = questions_gpt_each_dict["画面镜头模式"]
            camera_direction_str = post_with_retry_gpt35(api_key, camera_direction_choose_questions_gpt, txt_each, max_retries)
            camera_direction_num = sd_json['camera_direction_num']
            print("画面镜头:", camera_direction_str)
            print("画面镜头自动分析完毕")

    # CloseAI
    if "api.closeai-proxy.xyz" in api_url:
        # print(closeai)
        text = post_with_retry_CloseAI(api_key, questions_gpt, txt_each, max_retries)
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：", text)
        # 人物描述
        if sd_json["lora_describe_choose"] == "全自动":
            lora_describe_choose_questions_gpt = questions_gpt_each_dict["人物描述模式"]
            lora_describe = post_with_retry_CloseAI(api_key, lora_describe_choose_questions_gpt, txt_each, max_retries)
            # print("人物描述:", lora_describe)
            print("人物描述自动分析完毕")
        # 拍摄方法
        if sd_json["filming_method_choose"] == "全自动":
            filming_method_choose_questions_gpt = questions_gpt_each_dict["拍摄方法模式"]
            filming_method_str = post_with_retry_CloseAI(api_key, filming_method_choose_questions_gpt, txt_each, max_retries)
            filming_method_num = sd_json['filming_method_num']
            # print("拍摄方法:", filming_method_str)
            print("拍摄方法自动分析完毕")
        # 画面镜头
        if sd_json["camera_direction_choose"] == "全自动":
            camera_direction_choose_questions_gpt = questions_gpt_each_dict["画面镜头模式"]
            camera_direction_str = post_with_retry_CloseAI(api_key, camera_direction_choose_questions_gpt, txt_each, max_retries)
            camera_direction_num = sd_json['camera_direction_num']
            # print("画面镜头:", camera_direction_str)
            print("画面镜头自动分析完毕")

    # ClaudeAI【free】
    if "claude.ai" in api_url:
        # print(closeai)
        text = post_with_retry_ClaudeAI_Free(questions_gpt, txt_each, max_retries)
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：", text)
        # 人物描述
        if sd_json["lora_describe_choose"] == "全自动":
            lora_describe_choose_questions_gpt = questions_gpt_each_dict["人物描述模式"]
            lora_describe = post_with_retry_ClaudeAI_Free(lora_describe_choose_questions_gpt, txt_each, max_retries)
            # print("人物描述:", lora_describe)
            print("人物描述自动分析完毕")
        # 拍摄方法
        if sd_json["filming_method_choose"] == "全自动":
            filming_method_choose_questions_gpt = questions_gpt_each_dict["拍摄方法模式"]
            filming_method_str = post_with_retry_ClaudeAI_Free(filming_method_choose_questions_gpt, txt_each, max_retries)
            filming_method_num = sd_json['filming_method_num']
            # print("拍摄方法:", filming_method_str)
            print("拍摄方法自动分析完毕")
        # 画面镜头
        if sd_json["camera_direction_choose"] == "全自动":
            camera_direction_choose_questions_gpt = questions_gpt_each_dict["画面镜头模式"]
            camera_direction_str = post_with_retry_ClaudeAI_Free(camera_direction_choose_questions_gpt, txt_each, max_retries)
            camera_direction_num = sd_json['camera_direction_num']
            # print("画面镜头:", camera_direction_str)
            print("画面镜头自动分析完毕")

    # ClaudeAI【pay】
    if "api.anthropic.com" in api_url:
        # print(closeai)
        text = post_with_retry_ClaudeAI_Pay(questions_gpt, txt_each, max_retries)
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述关键词：", text)
        # 人物描述
        if sd_json["lora_describe_choose"] == "全自动":
            lora_describe_choose_questions_gpt = questions_gpt_each_dict["人物描述模式"]
            lora_describe = post_with_retry_ClaudeAI_Pay(lora_describe_choose_questions_gpt, txt_each, max_retries)
            # print("人物描述:", lora_describe)
            print("人物描述自动分析完毕")
        # 拍摄方法
        if sd_json["filming_method_choose"] == "全自动":
            filming_method_choose_questions_gpt = questions_gpt_each_dict["拍摄方法模式"]
            filming_method_str = post_with_retry_ClaudeAI_Pay(filming_method_choose_questions_gpt, txt_each, max_retries)
            filming_method_num = sd_json['filming_method_num']
            # print("拍摄方法:", filming_method_str)
            print("拍摄方法自动分析完毕")
        # 画面镜头
        if sd_json["camera_direction_choose"] == "全自动":
            camera_direction_choose_questions_gpt = questions_gpt_each_dict["画面镜头模式"]
            camera_direction_str = post_with_retry_ClaudeAI_Pay(camera_direction_choose_questions_gpt, txt_each, max_retries)
            camera_direction_num = sd_json['camera_direction_num']
            # print("画面镜头:", camera_direction_str)
            print("画面镜头自动分析完毕")

    # 百度直译【Free】
    if "fanyi.baidu.com" in api_url:
        # print(11111111111111)
        text = ts.translate_text(txt_each, to_language='en')
        print("开始生成关键词：【{}】".format(txt_each))
        print("画面描述直接翻译结果：", text)

    # 作者画风
    author_style_str = sd_json['author_style_str']
    author_style_num = sd_json['author_style_num']
    # 模式选择
    model_choose_str = sd_json['model_choose_str']
    model_choose_num = sd_json['model_choose_num']
    # 时代背景选择
    time_backgroud_str = sd_json['time_backgroud_str']
    time_backgroud_num = sd_json['time_backgroud_num']
    # 视觉效果、情感或氛围
    composition_method_str = sd_json['composition_method_str']
    composition_method_num = sd_json['composition_method_num']
    # 动态强度
    sense_speed_num = sd_json['sense_speed_num']
    # 氛围效果
    picture_atmosphere_num = sd_json['picture_atmosphere_num']

    # print("=" * 50)
    # print("author_style:", author_style(author_style_str), author_style_num)
    # print("model_choose:", model_choose(model_choose_str), model_choose_num)
    # print("time_backgroud:", time_backgroud(time_backgroud_str), time_backgroud_num)
    # print("camera_direction:", camera_direction(camera_direction_str), camera_direction_num)
    # print("filming_method:", filming_method(filming_method_str), filming_method_num)
    # print("composition_method:", composition_method(composition_method_str), composition_method_num)
    # print("sense_speed:", sense_speed_num)
    # print("picture_atmosphere:", picture_atmosphere_num)
    # print("=" * 50)

    # 获得结果拼接前缀词
    text = text_temp + "," + lora_describe + "," + text + "," + prompt + "," + \
           '(' * author_style_num + author_style(author_style_str) + ')' * author_style_num + "," + \
           '(' * model_choose_num + model_choose(model_choose_str) + ')' * model_choose_num + "," + \
           '(' * time_backgroud_num + time_backgroud(time_backgroud_str) + ')' * time_backgroud_num + "," + \
           '(' * camera_direction_num + camera_direction(camera_direction_str) + ')' * camera_direction_num + "," + \
           '(' * filming_method_num + filming_method(filming_method_str) + ')' * filming_method_num + "," + \
           '(' * composition_method_num + composition_method(composition_method_str) + ')' * composition_method_num + "," + \
           sense_speed(sense_speed_num) + "," + picture_atmosphere(picture_atmosphere_num)

    # 去除中文字符
    # text = re.sub('[\u4e00-\u9fa5]', '', text)
    text = re.sub('Prompt:', '', text)
    text = re.sub('Prompt', '', text)
    text = re.sub(r'[^\x00-\xff]', '', text)  # 替换中文符号
    # text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)  # 替换所有不可见字符

    # 字符串去重操作
    # 找到所有的英文单词
    words = re.findall(r'\b\w+\b', text)
    # 创建一个集合保存已经出现过的单词
    seen = set()
    # 对每个单词进行处理
    for word in words:
        if word not in seen:
            seen.add(word)
        else:
            # 如果单词已经出现过，那么替换为一个空字符串
            text = re.sub(r'\b' + word + r'\b', '', text, 1)

    text = clean_txt(text)
    text = text.replace('(),', '')
    text = text.replace(',,', ',')
    text = text.replace('  ', ' ')
    # text = text.replace(', ', '')
    text = text.replace("background:", ",")
    text = text.replace("character:", ",")
    text = clean_txt(text)

    print("生成关键词结束：【{}】".format(txt_each))
    print("最终生成关键词：{}".format(text))
    print("-" * 50)

    return text, negative


"""绘画风格关键信息"""


# 清理关键词中多余的逗号
def clean_txt(string):
    pattern = r',+(\s*,+)*'
    string = re.sub(pattern, ',', string)
    pattern = r'\s+,'
    return re.sub(pattern, ',', string)


# 通用num随机方法
def random_num(num_max):
    return random.randint(1, num_max)


# 作者画风
def author_style(author_style_str):
    author_style_dict = {
        "不选择": "",
        "《黑暗骑士归来》": "Frank Miller",
        "《超现实疯人院》": "Shintaro Kago",
        "《小林家的龙女仆》": "Ryohka",
        "《红翼机器人》": "J.C. Leyendecker",
        "《魔戒》": "Rebecca Guay",
        "《未来战士》": "Sachin Teng",
        "《Halo 4》": "Craig Mullins",
        "《Beck》": "Osamu Kobayashi",
        "《妖怪手表》": "Shigeru Mizuki",
        "《浪客剑心》": "Ryoichi Ikegami",
        "《狼的孩子雨和雪》": "Mamoru Hosoda",
        "《死神》": "Tite Kubo",
        "《你的名字。》": "Makoto Shinkai",
        "《美少女战士》": "Naoko Takeuchi",
        "《魔神凯撒》": "Gō Nagai",
        "《龙珠》": "Akira Toriyama",
        "《阿拉蕾》、《大王小王》": "Osamu Tezuka",
        "《犬夜叉》、《美少女战士》": "Rumiko Takahashi",
        "《新世纪福音战士》": "Hideaki Anno",
        "《AKIRA》": "Katsuhiro Otomo",
        "《龙猫》、《千与千寻》": "Hayao Miyazaki",
        "《借物少女艾莉緹》": "Hiromasa Yonebayashi",
        "《千年女优》": "Satoshi Kon",
        "《夜明前的琉璃色》": "Masaaki Yuasa",
        "《魔女宅急便》": "Kazuo Oga",
        "《声之形》、《春物》": "Naoko Yamada",
        "《SLAM DUNK》、《Code Geass 反叛的鲁路修》": "Takahiro Kimura",
        "《火影忍者》": "Masashi Kishimoto",
        "《白雪公主与七个小矮人》、《小飞象》": "Walt Disney",
        "《绵羊出击》系列、《机器鸟历险记》": "Nick Park",
        "《玩具总动员》系列、《海底总动员》": "John Lasseter",
        "《暗夜奇遇记》、《魔发奇缘》": "Tim Burton",
        "《美女与野兽》、《小鹿斑比》": "Glen Keane",
        "《史蒂文·尤妮佩》": "Rebecca Sugar",
        "《邪恶力量》、《星球大战：克隆人战争》": "Genndy Tartakovsky",
        "《布兰之谷》、《海洋之歌》": "Tomm Moore",
        "《汤姆猫和杰瑞鼠》": "Chuck Jones",
        "《火垂るの墓》": "Isao Takahata",
        "《三个老头的疯狂旅程》": "Sylvain Chomet",
        "《超人总动员》、《无敌破坏王》": "Brad Bird",
        "《珍爱生命》": "Marjane Satrapi",
        "《幸福工厂》": "Steve Cutts",
        "《红龙的夏天》": "Michael Dudok de Wit",
        "《疯狂农场》": "Aardman Animations",
        "《胡桃夹子》、《这不是一支烟斗》": "René Magritte",
        "涂鸦艺术《生命之舞》": "Keith Haring"
    }
    return author_style_dict.get(author_style_str, '')


# 时代背景选择
def time_backgroud(time_backgroud_str):
    time_backgroud_dict = {
        "不选择": "",
        "中世纪": "Middle Ages",
        "文艺复兴": "Renaissance",
        "日本明治時代": "Meiji Period",
        "工业革命": "Industrial Revolution",
        "日本江戸時代": "Edo Period",
        "繁华的二十年代": "Roaring Twenties",
        "冷战时期": "Cold War era",
        "信息时代": "Information Age",
        "中华宋朝": "Song Dynasty",
        "数字时代": "Digital Age",
        "中华战国时期": "Warring States Period",
        "青铜时代": "Bronze Age",
        "铁器时代": "Iron Age",
        "古典时代": "Classical Antiquity",
        "维多利亚时代": "Victorian Era",
        "镀金时代": "Gilded Age",
        "爵士时代": "Jazz Age",
        "太空时代": "Space Age",
        "古埃及": "Ancient Egypt",
        "好莱坞黄金时代": "Golden Age of Hollywood",
        "中华唐朝": "Tang Dynasty",
        "后现代主义": "Post-Modernism",
        "平和年代": "Era of Good Feelings",
        "启蒙时代": "Age of Enlightenment",
        "哥特式时期": "Gothic Period",
        "探险时代": "Age of Exploration",
        "中华明朝": "Ming Dynasty",
        "原子时代": "Atomic Age",
        "现代主义": "Modernism"
    }
    return time_backgroud_dict.get(time_backgroud_str, '')


# 画面镜头
def camera_direction(camera_direction_str):
    camera_direction_dict = {
        '不选择': '',
        '向左': 'Left',
        '向右': 'Right',
        '向上': 'Up',
        '向下': 'Down',
        '向前': 'Forward',
        '向后': 'Backward',
        '北方': 'North',
        '南方': 'South',
        '东方': 'East',
        '西方': 'West',
        '东北方': 'Northeast',
        '西北方': 'Northwest',
        '东南方': 'Southeast',
        '西南方': 'Southwest',
        '水平的': 'Horizontal',
        '垂直的': 'Vertical',
        '对角线的': 'Diagonal',
        '升序的': 'Ascending',
        '降序的': 'Descending',
        '顺时针方向的': 'Clockwise'
    }
    if camera_direction_str == '随机':
        del camera_direction_dict['不选择']
        return random.choice(list(camera_direction_dict.values()))
    else:
        return camera_direction_dict.get(camera_direction_str, '')


# 拍摄方法
def filming_method(filming_method_str):
    filming_method_dict = {
        "不选择": "",
        "特写镜头": "Close-up",
        "螃蟹镜头": "crab shot",
        "地板水平镜头": "floor level shot",
        "膝盖水平镜头": "knee-level shot",
        "臀部水平镜头": "hip-level shot",
        "万花筒镜头": "kaleidoscope shot",
        "红外线镜头": "infrared shot",
        "热成像镜头": "thermal imaging shot",
        "鸟瞰图": "Bird's eye view",
        "高角度镜头": "High angle shot",
        "蚯蚓视角镜头": "Worm's eye view",
        "上帝视角镜头": "God's eye view",
        "无人机镜头": "drone shot",
        "子弹时间镜头": "bullet time shot",
        "斯诺里卡姆镜头": "snorricam shot",
        "移轴镜头": "tilt-shift shot",
        "变形镜头": "anamorphic shot",
        "360度镜头": "360-degree shot",
        "空中镜头": "aerial shot",
        "望远镜镜头": "telescopic shot",
        "显微镜镜头": "microscopic shot",
        "胸部水平镜头": "chest-level shot",
        "天空水平镜头": "sky-level shot",
        "水下镜头": "under-water shot",
        "分光镜头": "split diopter shot",
        "低调镜头": "low-key shot",
        "高调镜头": "high-key shot",
        "剪影镜头": "silhouette shot",
        "夜视镜头": "night vision shot",
        "慢动作镜头": "slow motion shot",
        "极端特写镜头": "extreme close-up",
        "中特写镜头": "medium close-up",
        "中景镜头": "medium shot",
        "中长景镜头": "medium long shot",
        "长景镜头": "long shot",
        "极长景镜头": "extreme long shot",
        "全景镜头": "full shot",
        "牛仔镜头": "cowboy shot",
        "鸟瞰视角": "bird's eye view",
        "蚯蚓视角": "worm's eye view",
        "高角度": "high angle",
        "低角度": "low angle",
        "荷兰角度": "Dutch angle",
        "正面角度": "straight-on angle",
        "肩膀后方镜头": "over-the-shoulder shot",
        "视角镜头": "point-of-view shot",
        "两人镜头": "two-shot",
        "三人镜头": "three-shot",
        "建立镜头": "establishing shot",
        "插曲镜头": "cutaway shot",
        "反应镜头": "reaction shot",
        "插入镜头": "insert shot",
        "屏幕外镜头": "off-screen shot",
        "反角度镜头": "reverse angle",
        "底部镜头": "bottom shot",
        "倾斜镜头": "tilt shot",
        "平移镜头": "pan shot",
        "放大镜头": "zoom in shot",
        "缩小镜头": "zoom out shot",
        "推进镜头": "dolly in shot",
        "拉远镜头": "dolly out shot",
        "跟踪镜头": "tracking shot",
        "稳定器镜头": "steadicam shot",
        "手持镜头": "handheld shot",
        "起重镜头": "crane shot",
        "航拍镜头": "aerial shot",
        "分屏镜头": "split screen shot",
        "静帧镜头": "freeze frame shot"
    }
    if filming_method_str == '随机':
        del filming_method_dict['不选择']
        return random.choice(list(filming_method_dict.values()))
    else:
        return filming_method_dict.get(filming_method_str, '')


# 视觉效果、情感或氛围
def composition_method(composition_method_str):
    composition_method_dict = {
        "不选择": "",
        "迷人的": "captivating",
        "令人着迷的": "mesmerizing",
        "令人神魂颠倒的": "spellbinding",
        "引人注目的": "striking",
        "诱人的": "alluring",
        "阴影的": "shadowy",
        "威胁的": "menacing",
        "怪异的": "eerie",
        "难以捉摸的": "elusive",
        "有趣的": "intriguing",
        "深思的": "contemplative",
        "反思的": "reflective",
        "唤起情感的": "evocative",
        "忧伤的": "wistful",
        "沉思的": "pensive",
        "平静的": "calm",
        "宁静的": "placid",
        "骚乱的": "tumultuous",
        "狂乱的": "frenetic",
        "令人困惑的": "bewildering",
        "如梦似幻的": "dreamlike",
        "神秘的": "mystical",
        "飘渺的": "ethereal"
    }

    if composition_method_str == '随机':
        del composition_method_dict['不选择']
        return random.choice(list(composition_method_dict.values()))
    else:
        return composition_method_dict.get(composition_method_str, '')


# 画面氛围【负数恐怖阴暗，正数明亮乐观】
def picture_atmosphere(picture_atmosphere_num):
    if picture_atmosphere_num == 0:
        return ""
    elif picture_atmosphere_num < 0:
        return '(' * abs(picture_atmosphere_num) + '(Horror, gloomy visuals),' + ')' * abs(picture_atmosphere_num)
    else:
        return '(' * picture_atmosphere_num + 'Sunshine, optimistic visuals,' + ')' * picture_atmosphere_num


# 动态强度，需要填写整数
def sense_speed(sense_speed_num):
    if sense_speed_num == 0:
        return ""
    else:
        return '(' * sense_speed_num + 'Sense of speed' + ')' * sense_speed_num


# 选择模式
def model_choose(model_choose_str):
    mtt1 = "Split black and white manuscript，Black and white comics, Black and white stories,"
    mtt2 = "Craig Mullins, Dynamic segmentation,Best composition,Best story expression, Best visual expression,Best composition, "
    model_choose_dict = {
        '不选择': "",
        '漫画模式': "Movie s hots,stone," + random.choice(mtt1.split(",")),
        '电影分镜': "Movie s hots,stone," + random.choice(mtt2.split(",")),
    }
    return model_choose_dict.get(model_choose_str, '')


# 均分txt_list
def split_list(lst, n):
    avg = len(lst) // n
    remainder = len(lst) % n
    result = []
    start = 0
    for i in range(n):
        if i < remainder:
            end = start + avg + 1
        else:
            end = start + avg
        result.append(lst[start:end])
        start = end
    return result


# 依据GPT处理关键词
def process_menu_number(txt_new_list, api_url, api_key, max_retries, retry_time, questions_gpt, sd_json,
                        lora_dict, TaskEach):
    for each in txt_new_list:
        txt_each = each.txt
        id_ = each.id
        text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                        sd_json, lora_dict)
        TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
        time.sleep(0.5)


# 批量处理全部记录
def step_2_function(num, Task, TaskEach):
    # 获取用户信息
    result_info = user_authenticate()
    print(result_info["msg"])

    # ChatGPT验证
    chat_gpt_dict = get_chat_gpt_model()
    api_url = chat_gpt_dict['api_url']
    max_retries = chat_gpt_dict['max_retries']
    retry_time = None if chat_gpt_dict['retry_time'] == 0 else chat_gpt_dict['retry_time']
    questions_gpt = questions_gpt_dict[chat_gpt_dict['questions_gpt']]
    # print(chat_gpt_dict)

    # SD验证
    sd_json = get_stable_diffusion_model()
    # print(sd_json)

    if '用户验证通过' in result_info["msg"]:
        if "zhishuyun.com" in api_url:
            api_key_list = list(GPT_ZSY.objects.values_list('api_key', flat=True))
        elif "openai.com" in api_url:
            api_key_list = list(GPT_OPENAI.objects.values_list('api_key', flat=True))
        elif "api.closeai-proxy.xyz" in api_url:
            api_key_list = list(GPT_CLOSEAI.objects.values_list('api_key', flat=True))

        # 判断是否是自定义关键词
        if chat_gpt_dict["questions_gpt"] == "自定义组合":
            questions_gpt["question_txt_1"] = chat_gpt_dict["questions_txt_1"]
            questions_gpt["question_txt_2"] = chat_gpt_dict["questions_txt_2"]

        data_list = Task.objects.filter(id=num)

        print("使用openai的用户验证成功请抓紧切换代理")
        print("这里设置了3秒延迟，任务在3秒后开启")
        time.sleep(3)

        # print(data_list)
        for data in data_list:
            cn_name = data.cn_name
            en_name = data.en_name
            type_path = data.type
            task_id = data.id
            lora_dict = Task.objects.filter(id=task_id)[0].lora_temp
            if lora_dict:
                print("使用自定义Lora")
            else:
                print("配置中没有自定义Lora")
            # 获取这个任务id所有的任务列表
            txt_list = TaskEach.objects.filter(Q(task_id=task_id) & Q(prompt='待处理'))

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
                        txt_new_list, api_url, api_key, max_retries, retry_time, questions_gpt, sd_json, lora_dict,
                        TaskEach))
                    thread.start()

            elif "zhishuyun.com" in api_url:
                # print(txt_list)
                api_key = api_key_list[0]
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                                    sd_json, lora_dict)
                    TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
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
                        txt_new_list, api_url, api_key, max_retries, retry_time, questions_gpt, sd_json, lora_dict,
                        TaskEach))
                    thread.start()

            elif "claude.ai" in api_url:
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    api_key = ""
                    text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                                    sd_json, lora_dict)
                    TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
                    time.sleep(0.5)

            elif "api.anthropic.com" in api_url:
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    api_key = ""
                    text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                                    sd_json, lora_dict)
                    TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
                    time.sleep(0.5)

            elif "fanyi.baidu.com" in api_url:
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    api_key = ""
                    text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                                    sd_json, lora_dict)
                    TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
                    time.sleep(0.5)

        data_len_txt = "无待处理文本生成描述关键词" if len(txt_list) == 0 else "生成关键词条目：{}".format(len(txt_list))

        print_info = [
            "生成关键词描述完毕",
            data_len_txt,
            "文章类别：{}".format(data.type),
            "英文名称：{}".format(data.en_name),
            "中文名称：{}".format(data.cn_name),
        ]

        print_with_border(print_info)


# 重制单条记录
def step_2_1_function(num, index):
    # 获取用户信息
    result_info = user_authenticate()
    print(result_info["msg"])

    # ChatGPT验证
    chat_gpt_dict = get_chat_gpt_model()
    api_url = chat_gpt_dict['api_url']
    max_retries = chat_gpt_dict['max_retries']
    retry_time = None if chat_gpt_dict['retry_time'] == 0 else chat_gpt_dict['retry_time']
    questions_gpt = questions_gpt_dict[chat_gpt_dict['questions_gpt']]
    # print(chat_gpt_dict)

    # SD验证
    sd_json = get_stable_diffusion_model()
    # print(sd_json)

    if '用户验证通过' in result_info["msg"]:
        if "zhishuyun.com" in api_url:
            api_key_list = list(GPT_ZSY.objects.values_list('api_key', flat=True))
        elif "openai.com" in api_url:
            api_key_list = list(GPT_OPENAI.objects.values_list('api_key', flat=True))
        elif "api.closeai-proxy.xyz" in api_url:
            api_key_list = list(GPT_CLOSEAI.objects.values_list('api_key', flat=True))

        # 判断是否是自定义关键词
        if chat_gpt_dict["questions_gpt"] == "自定义组合":
            questions_gpt["question_txt_1"] = chat_gpt_dict["questions_txt_1"]
            questions_gpt["question_txt_2"] = chat_gpt_dict["questions_txt_2"]

        data_list = Task.objects.filter(id=num)

        print("使用openai的用户验证成功请抓紧切换代理")
        print("这里设置了3秒延迟，任务在3秒后开启")
        time.sleep(3)

        # print(data_list)
        for data in data_list:
            cn_name = data.cn_name
            en_name = data.en_name
            type_path = data.type
            task_id = data.id
            lora_dict = Task.objects.filter(id=task_id)[0].lora_temp
            if lora_dict:
                print("使用自定义Lora")
            else:
                print("配置中没有自定义Lora")
            # 获取这个任务id所有的任务列表
            txt_list = TaskEach.objects.filter(Q(task_id=task_id) & Q(index=index))

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
                        txt_new_list, api_url, api_key, max_retries, retry_time, questions_gpt, sd_json, lora_dict,
                        TaskEach))
                    thread.start()

            elif "zhishuyun.com" in api_url:
                # print(txt_list)
                api_key = api_key_list[0]
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                                    sd_json, lora_dict)
                    TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
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
                        txt_new_list, api_url, api_key, max_retries, retry_time, questions_gpt, sd_json, lora_dict,
                        TaskEach))
                    thread.start()

            elif "claude.ai" in api_url:
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    api_key = ""
                    text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                                    sd_json, lora_dict)
                    TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
                    time.sleep(0.5)

            elif "api.anthropic.com" in api_url:
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    api_key = ""
                    text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                                    sd_json, lora_dict)
                    TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
                    time.sleep(0.5)

            elif "fanyi.baidu.com" in api_url:
                for each in txt_list:
                    txt_each = each.txt
                    id_ = each.id
                    api_key = ""
                    text, negative = get_gpt35_text(txt_each, api_url, api_key, max_retries, retry_time, questions_gpt,
                                                    sd_json, lora_dict)
                    TaskEach.objects.filter(id=id_).update(prompt=text, negative=negative)
                    time.sleep(0.5)

        data_len_txt = "无待处理文本生成描述关键词" if len(txt_list) == 0 else "生成关键词条目：{}".format(len(txt_list))

        print_info = [
            "生成关键词描述完毕",
            data_len_txt,
            "文章类别：{}".format(data.type),
            "英文名称：{}".format(data.en_name),
            "中文名称：{}".format(data.cn_name),
        ]

        print_with_border(print_info)

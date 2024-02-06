# -*- coding: UTF-8 -*-
import json
import re
import random
import hashlib
import platform
import uuid
import requests
from requests.exceptions import RequestException
import time
from Data.models import *
from Config.models import *


user_info = UserInfo.objects.first()
username = user_info.username
password = user_info.password
UserData = {
    'username': username,
    'password': password,
}


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


def get_prompt_num(UserData):
    # 定义请求的 URL
    url = 'http://url/User/UserManagerView2/?user_name={}'.format(UserData['username'])
    # url = 'http://192.168.110.234/User/UserManagerView2/?user_name={}'.format(UserData['username'])
    # 发送 POST 请求
    response = requests.get(url)
    result = json.loads(response.text)
    return result


# 用户网络验证环节
def user_authenticate(UserData):
    # print(UserData)
    # 定义请求的 URL
    url = 'http://url/User/UserManagerView2/'
    # url = 'http://192.168.110.234/User/UserManagerView2/'
    # 发送 POST 请求
    response = requests.post(url, data=UserData)
    # print(11111111111)
    # print(response.text)
    # 解析响应
    if response.status_code == 200:
        result = json.loads(response.text)
        return result
    else:
        return "验证未通过，请联系管理员"


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
}


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
            print(f"GPT35生成关键词失败，尝试启动第 {retries}/{max_retries} 次")
            time.sleep(3)
    print(f"重试次数超过 ({max_retries}) 次，你的网太烂了，重来吧")
    return None


def post_with_retry_gpt35(u, p, text):
    url = "http://43.153.109.77:5000/NovelAIGPT"

    data = {
        "username": u,
        "password": p,
        "txt_each": text
    }

    html = requests.post(url, json=data).text
    return html


def get_gpt35_text(u, p, text, sd_json):
    # 这里写访问服务器的逻辑
    text = post_with_retry_gpt35(u, p, text)

    print("开始生成关键词：【{}】".format(text))
    # print(text)
    print("生成关键词结束：【{}】".format(text))
    print("-" * 50)

    # 解析配置数据
    # 解析配置数据
    prompt = sd_json['prompt']  # SD正面词
    negative = sd_json['negative']  # SD负面词
    # num_max = sd_json['num_max']  # 通用随机最大数

    # 作者画风
    author_style_str = sd_json['author_style_str']
    author_style_num = sd_json['author_style_num']
    # 模式选择
    model_choose_str = sd_json['model_choose_str']
    model_choose_num = sd_json['model_choose_num']
    # 时代背景选择
    time_backgroud_str = sd_json['time_backgroud_str']
    time_backgroud_num = sd_json['time_backgroud_num']
    # 画面镜头
    camera_direction_str = sd_json['camera_direction_str']
    camera_direction_num = sd_json['time_backgroud_num']
    # 拍摄方法
    filming_method_str = sd_json['filming_method_str']
    filming_method_num = sd_json['filming_method_num']
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
    text = '(' * author_style_num + author_style(author_style_str) + ')' * author_style_num + "," + \
           '(' * model_choose_num + model_choose(model_choose_str) + ')' * model_choose_num + "," + \
           prompt + "," + text + "," + \
           '(' * time_backgroud_num + time_backgroud(time_backgroud_str) + ')' * time_backgroud_num + "," + \
           '(' * camera_direction_num + camera_direction(camera_direction_str) + ')' * camera_direction_num + "," + \
           '(' * filming_method_num + filming_method(filming_method_str) + ')' * filming_method_num + "," + \
           '(' * composition_method_num + composition_method(composition_method_str) + ')' * composition_method_num + "," + \
           sense_speed(sense_speed_num) + "," + picture_atmosphere(picture_atmosphere_num)

    # 去除中文字符
    text = re.sub('[\u4e00-\u9fa5]', '', text)
    text = clean_txt(text)
    # print(text)
    return text, negative


### 绘画风格关键信息 ###

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


def step_prompt(text, UserData):
    # 判断额度是否充足
    result_info = get_prompt_num(UserData)
    print(result_info["msg"])

    if '额度充足' in result_info["msg"]:
        # 获取用户gpt配置信息
        u = UserData["username"]
        p = UserData["password"]
        i = generate_unique_identifier()

        sd_url = "http://url/Setting/StableDiffusionView/?u={}&p={}&i={}".format(u, p, i)
        # print(sd_url)
        # sd_url = "http://192.168.110.234/Setting/StableDiffusionView/?u={}&p={}&i={}".format(u, p, i)
        html = requests.get(sd_url).text
        # print(html)
        sd_json = json.loads(html)['setting_data']
        # print(sd_json)
        gpt_url = "http://url/Setting/ChatGPT35View/?u={}&p={}&i={}".format(u, p, i)
        html = requests.get(gpt_url).text
        gpt_json = json.loads(html)['setting_data']
        # 获取SD配置中渐渐次的配置
        questions_gpt = questions_gpt_dict[gpt_json['questions_gpt']]
        # 判断是否是自定义关键词
        if gpt_json["questions_gpt"] == "自定义组合":
            questions_gpt["question_txt_1"] = gpt_json["questions_txt_1"]
            questions_gpt["question_txt_2"] = gpt_json["questions_txt_2"]

        # 构建提问的文本数据
        text_add = questions_gpt["question_txt_1"] + text + questions_gpt["question_txt_2"]
        # print(text)
        text_, negative = get_gpt35_text(u, p, text_add, sd_json)

        data = {
            "username": u,
            "password": p,
            "prompt_num": len(text),
            "content_cn": text,
            "content_en": text_
        }
        # 更新数据信息
        user_authenticate(data)


def get_prompt(UserData):
    # 获取用户gpt配置信息
    u = UserData["username"]
    p = UserData["password"]
    i = generate_unique_identifier()
    prompt_url = "http://datayang.cn:9999/User/UserManagerPrompt/?u={}&p={}&i={}".format(u, p, i)
    # prompt_url = "http://192.168.110.234/User/UserManagerPrompt/?u={}&p={}&i={}".format(u, p, i)
    html = requests.get(prompt_url).text
    # print(html)
    data_list = json.loads(html)
    data_list = sorted(data_list, key=lambda x: x['pk'], reverse=True)
    # print(len(data_list))
    return data_list

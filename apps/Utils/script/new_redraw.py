# -*- coding: UTF-8 -*-
'''
@Project ：sell_NovelAI_txt2video
@File    ：04.SD批量绘图
@IDE     ：PyCharm 
@Author  ：Mr数据杨
@Date    ：2023/4/24 16:09 
'''

import base64
from PIL import Image
from io import BytesIO
import json
from nsfw_model.nsfw_detector import predict
import os
import requests
import hashlib
import platform
import uuid
from Config.models import *
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
    # print(response)
    # print(response.text)
    # 解析响应
    if response.status_code == 200:
        result = json.loads(response.text)
        return result
    else:
        return "验证未通过，请联系管理员"


# 绘图API
def draw(txt_list, sd_json, num, type_path, en_name):
    # print(txt_list, num)
    # 构建AN绘画传参字典
    # print(txt_list[num].prompt)
    # print(txt_list[num].negative)
    if sd_json["adetailer"] == "true":
        novel_dict = {
            "prompt": txt_list[num].prompt,
            "negative_prompt": txt_list[num].negative,

            # 高清修复部分
            "enable_hr": sd_json['enable_hr'],
            "scale_latent": "true",
            "denoising_strength": sd_json['denoising_strength'],
            "hr_scale": 2,
            "hr_upscaler": sd_json['hr_upscaler'],
            "hr_second_pass_steps": sd_json['steps'],
            "hr_resize_x": int(sd_json['sd_image_width'] * sd_json['hr_resize_factor']),
            "hr_resize_y": int(sd_json['sd_image_height'] * sd_json['hr_resize_factor']),
            "firstphase_width": 0,
            "firstphase_height": 0,

            "styles": [
                "string"
            ],
            "seed": sd_json['seed'],
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "sampler_name": sd_json['sd_sampler'],
            "batch_size": 1,
            "n_iter": 1,
            "steps": sd_json['steps'],
            "cfg_scale": sd_json['cfg_scale'],
            "width": sd_json['sd_image_width'],
            "height": sd_json['sd_image_height'],
            "restore_faces": sd_json['restore_faces'],
            "tiling": "false",
            "do_not_save_samples": "false",
            "do_not_save_grid": "false",
            "eta": 0,
            "s_churn": 0,
            "s_tmax": 0,
            "s_tmin": 0,
            "s_noise": 1,
            "override_settings": {
                # "sd_model_checkpoint": "RealBackground_v12"
            },
            "override_settings_restore_afterwards": "true",
            "script_args": [],
            "sampler_index": sd_json['sd_sampler'],
            "script_name": "",
            "send_images": "true",
            "save_images": "true",
            "alwayson_scripts": {
                "ADetailer": {
                    'args': [
                        {
                            'ad_model': 'face_yolov8m.pt',
                            'ad_use_inpaint_width_height': True,
                            'ad_denoising_strength': 0.2,
                        },
                        {
                            'ad_model': 'hand_yolov8s.pt',
                            'ad_use_inpaint_width_height': True,
                            'ad_denoising_strength': 0.2,
                        }
                    ]
                },
            }
        }
    else:
        novel_dict = {
            "prompt": txt_list[num].prompt,
            "negative_prompt": txt_list[num].negative,

            # 高清修复部分
            "enable_hr": sd_json['enable_hr'],
            "scale_latent": "true",
            "denoising_strength": sd_json['denoising_strength'],
            "hr_scale": 2,
            "hr_upscaler": sd_json['hr_upscaler'],
            "hr_second_pass_steps": sd_json['steps'],
            "hr_resize_x": int(sd_json['sd_image_width'] * sd_json['hr_resize_factor']),
            "hr_resize_y": int(sd_json['sd_image_height'] * sd_json['hr_resize_factor']),
            "firstphase_width": 0,
            "firstphase_height": 0,

            "styles": [
                "string"
            ],
            "seed": sd_json['seed'],
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "sampler_name": sd_json['sd_sampler'],
            "batch_size": 1,
            "n_iter": 1,
            "steps": sd_json['steps'],
            "cfg_scale": sd_json['cfg_scale'],
            "width": sd_json['sd_image_width'],
            "height": sd_json['sd_image_height'],
            "restore_faces": sd_json['restore_faces'],
            "tiling": "false",
            "do_not_save_samples": "false",
            "do_not_save_grid": "false",
            "eta": 0,
            "s_churn": 0,
            "s_tmax": 0,
            "s_tmin": 0,
            "s_noise": 1,
            "override_settings": {
                # "sd_model_checkpoint": "RealBackground_v12"
            },
            "override_settings_restore_afterwards": "true",
            "script_args": [],
            "sampler_index": sd_json['sd_sampler'],
            "script_name": "",
            "send_images": "true",
            "save_images": "true",
            "alwayson_scripts": {}
        }

    # print(sd_json)
    # stable diffusion url
    sd_url = "http://{}/sdapi/v1/txt2img".format(sd_json["sd_url"])

    # 保存图片
    path_image = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "data_png")
    image_path = os.path.join(path_image, str(txt_list[num].index) + ".png")
    print("重绘图片完成", image_path)
    if os.path.exists(image_path):
        pass
    else:
        html = requests.post(sd_url, data=json.dumps(novel_dict))
        img_response = json.loads(html.text)
        # print(img_response)
        # 解码图片数据
        image_bytes = base64.b64decode(img_response['images'][0])
        # 将字节流转换为图片对象
        image = Image.open(BytesIO(image_bytes))
        image.save(image_path)
    return image_path


def draw_all(txt_list, num, type_path, en_name, UserData, sd_json):
    image_path = draw(txt_list, sd_json, num, type_path, en_name)
    # result = subprocess.run(['D:/MyTools/anaconda3/python.exe', 'nsfw/nsfw_predict.py', image_path],
    #                         stdout=subprocess.PIPE)
    # # 获取print输出
    # output = result.stdout.decode('utf-8')
    if sd_json["nsfw"] == "开启":
        model_path = os.path.join(BASE_DIR, "nsfw_model", "nsfw_mobilenet2.224x224.h5")
        model = predict.load_model(model_path)
        output = predict.classify(model, image_path)
        output_dict = list(output.items())[0][1]
        # 结果排序
        sorted_d = sorted(output_dict.items(), key=lambda x: x[1], reverse=True)
        # print(sorted_d)
        # 提取值并排序
        max_key = sorted_d[0][0]
        # print(max_key)

        if 'porn' == max_key:
            print(output)
            print("发现淫秽作品重画")
            output = draw_all(txt_list, num, type_path, en_name, UserData, sd_json)
        else:
            print(output)
            print("图片验证通过")


def step_4_2_fuction(num, type_path, en_name, index, Task, TaskEach):
    user_info = UserInfo.objects.first()
    username = user_info.username
    password = user_info.password
    UserData = {
        'username': username,
        'password': password,
    }
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
        # 先筛选项目
        task_id = Task.objects.filter(id=num).first().id
        # print(task_id)
        # print(TaskEach)
        data_list = TaskEach.objects.filter(task_id=task_id, index=index)
        # print(data_list)
        # txt_list = [data_list]
        # print(txt_list)
        num = 0
        # 先删除需要重绘的图片
        # print(data_list)
        remove_png_path = os.path.join(BASE_DIR, "Txt2Video", type_path, en_name, "data_png", data_list[num].index + ".png")
        print("删除重绘的图片")
        try:
            os.remove(remove_png_path)
        except:
            print("没有可以删除的图片")
        draw(data_list, sd_json, num, type_path, en_name)

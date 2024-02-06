# -*- coding: UTF-8 -*-
import os
import requests
import hashlib
import platform
import uuid
import json
import random
from Data.models import *
from Data1.models import *
from Config.models import *
from NovelAIUser.settings import *
from PIL import Image
import cv2
from moviepy.editor import *
import shutil
import random
import os
import subprocess

try:
    from apps.Utils.script.GeneralTools import *
except:
    from apps.Utils.pyd.GeneralTools import *


# 获取音频时长
def get_audio_duration(video):
    video_clip = VideoFileClip(video)
    duration = video_clip.duration
    return duration


def video_base_function():
    result_info = user_authenticate()
    print(result_info["msg"])

    if '用户验证通过' in result_info["msg"]:
        # 获取视频设置基础参数
        last_record = VideoBaseSetting.objects.last()
        # 使用values()方法将模型实例转换为字典
        last_record_dict = last_record.__dict__
        # 删除不必要的键 '_state'，它不是模型字段
        del last_record_dict['_state'], last_record_dict['id']

        # 获取全部设置的参数值
        fps = last_record_dict['fps']
        brightness_num = last_record_dict['brightness_num']
        saturation_num = last_record_dict['saturation_num']
        contrast_num = last_record_dict['contrast_num']
        unsharp_l_msize_x = last_record_dict['unsharp_l_msize_x']
        unsharp_l_msize_y = last_record_dict['unsharp_l_msize_y']
        unsharp_l_amount = last_record_dict['unsharp_l_amount']
        hqdn3d_luma_spatial = last_record_dict['hqdn3d_luma_spatial']
        hqdn3d_chroma_spatia = last_record_dict['hqdn3d_chroma_spatia']
        hqdn3d_luma_tmp = last_record_dict['hqdn3d_luma_tmp']
        hqdn3d_chroma_tmp = last_record_dict['hqdn3d_chroma_tmp']
        scale = last_record_dict['scale']
        scale__x = last_record_dict['scale_x']
        scale__y = last_record_dict['scale_y']
        transpose = last_record_dict['transpose']
        frame_set = last_record_dict['frame_set']
        frame_set_max = last_record_dict['frame_set_max']
        frame_set_min = last_record_dict['frame_set_min']

        # 亮度，饱和度，对比度方法
        # brightness_num = 0.2  # 将亮度增加 [-1 - 1]
        # saturation_num = 1.5  # 将饱和度增加 [0 - 3]
        # contrast_num = 1.2  # 将对比度增加 [-2 - 2]
        function_eq = "eq=brightness={}:saturation={}:contrast={}".format(brightness_num, saturation_num, contrast_num)

        # 锐化
        # unsharp_l_msize_x = 5  # X方向的锐化半径 [3 - 23]
        # unsharp_l_msize_y = 5  # Y方向的锐化半径 [3 - 23]
        # unsharp_l_amount = 5  # 锐化强度 [-2 - 5]
        function_eunsharp = "unsharp={}:{}:{}".format(unsharp_l_msize_x, unsharp_l_msize_y, unsharp_l_amount)

        # 降噪
        # hqdn3d_luma_spatial = 1.5  # 空间降噪强度，较大的值会增加降噪效果。
        # hqdn3d_chroma_spatia = 1.5  # 色度通道空间降噪强度，较大的值会增加降噪效果。
        # hqdn3d_luma_tmp = 6  # 时间降噪强度，较大的值会增加降噪效果。
        # hqdn3d_chroma_tmp = 6  # 色度通道时间降噪强度，较大的值会增加降噪效果。
        function_hqdn3d = "hqdn3d={}:{}:{}:{}".format(hqdn3d_luma_spatial, hqdn3d_chroma_spatia, hqdn3d_luma_tmp, hqdn3d_chroma_tmp)

        if scale == "自定义":
            scale_x, scale_y = scale__x, scale__y
            function_scale = "scale={}:{}".format(scale_x, scale_y)
        else:
            # 分辨率处理
            scale_dict = {
                "480P": {"scale_x": "854", "scale_y": "480"},
                "720P": {"scale_x": "1280", "scale_y": "720"},
                "1080P": {"scale_x": "1920", "scale_y": "1080"},
                "横竖互换": {"scale_x": "ih", "scale_y": "iw"},
            }

            scale_x, scale_y = scale_dict[scale]["scale_x"], scale_dict[scale]["scale_y"]
            function_scale = "scale={}:{}".format(scale_x, scale_y)

        # 视频拉伸默认
        function_setdar = "setsar=1"

        # 视频旋转
        transpose_dict = {
            "逆时针旋转90度": "transpose=1",
            "顺时针旋转90度": "transpose=2",
            "水平旋转": "hflip",
            "垂直旋转": "vflip",
            "不操作": ""
        }
        function_transpose = transpose_dict[transpose]

        # 视频抽帧
        frame_set_random = random.randint(frame_set_min, frame_set_max)
        function_select_v = "select='(mod(n\,{}))',setpts=N/FRAME_RATE/TB".format(frame_set_random)
        function_select_a = "aselect='(mod(n\,{}))',asetpts=N/SR/TB".format(frame_set_random)

        # 放大的暂时没用
        zoom_in = "zoompan=z='if(lte(on,100),zoom+0.01,1.5)':x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':d=1, fade=in:st=0:d=1:alpha=1, fade=out:st=99:d=1:alpha=1"

        # 获取需要处理的视频列表
        video_dir = os.path.join(BASE_DIR, "VideoProcess", "video", "base")
        video_list = os.listdir(video_dir)
        # 在result下创建项目,批量处理
        for video_file in video_list:
            # 被处理的视频文件路径
            video_path = os.path.join(video_dir, video_file)
            # 数据处理保存文件的目录
            video_each_dir = os.path.join(BASE_DIR, "VideoProcess", "result", video_file)
            if not os.path.exists(video_each_dir):
                os.makedirs(video_each_dir)
            base_result_file = os.path.join(video_each_dir, "base_result.mp4")

            if frame_set == "设置抽帧":
                function_vf = ", ".join([
                    function_eq,  # 亮度，饱和度，对比度方法
                    function_eunsharp,  # 锐化
                    function_hqdn3d,  # 降噪
                    function_scale,  # 分辨率处理
                    function_setdar,  # 视频拉伸
                    function_transpose,  # 视频旋转
                    function_select_v,  # 视频抽帧
                    # zoom_in,  # 逐帧放大
                ])
                function_af = ",".join([
                    function_select_a  # 视频抽帧保持原音频匹配
                ])
                cmd = 'ffmpeg -y -i {} -vf "{} " -af "{}" -r {}  {}'.format(
                    video_path, function_vf, function_af, fps, base_result_file
                )
            else:
                function_vf = ", ".join([
                    function_eq,  # 亮度，饱和度，对比度方法
                    function_eunsharp,  # 锐化
                    function_hqdn3d,  # 降噪
                    function_scale,  # 分辨率处理
                    function_setdar,  # 视频拉伸
                    function_transpose,  # 视频旋转
                    # function_select_v,  # 视频抽帧
                    # zoom_in,  # 逐帧放大
                ])
                cmd = 'ffmpeg -y -i {} -vf "{} " -r {}  {}'.format(
                    video_path, function_vf, fps, base_result_file
                )

            os.system(cmd)

    print("全部视频处理完毕")


def video_base_insert_function():
    result_info = user_authenticate()
    print(result_info["msg"])
    # 图片路径
    # print(MediaDir)
    # print(request)

    if '用户验证通过' in result_info["msg"]:
        # 获取视频设置基础参数
        last_record = FrameProcess.objects.last()
        # 使用values()方法将模型实例转换为字典
        last_record_dict = last_record.__dict__
        # 删除不必要的键 '_state'，它不是模型字段
        del last_record_dict['_state'], last_record_dict['id']

        fps = last_record_dict['fps']
        frame_insert_num = last_record_dict['frame_insert_num']
        blend_num = last_record_dict['blend_num']
        add_min_count = last_record_dict['add_min_count']
        add_max_count = last_record_dict['add_max_count']

        # 获取需要处理的视频列表
        video_dir = os.path.join(BASE_DIR, "VideoProcess", "video", "base")
        video_list = os.listdir(video_dir)

        # 获取插帧素材文件
        image_dir = os.path.join(BASE_DIR, "VideoProcess", "video", "image")
        image_list = os.listdir(image_dir)

        # 在result下创建项目,批量处理
        for video_file in video_list:
            # 被处理的视频文件路径
            video_path = os.path.join(video_dir, video_file)
            # 数据处理保存文件的目录
            video_each_dir = os.path.join(BASE_DIR, "VideoProcess", "result", video_file)
            if not os.path.exists(video_each_dir):
                os.makedirs(video_each_dir)
            # 创建frame目录
            video_each_insert_dir = os.path.join(video_each_dir, "insert_frame")
            if not os.path.exists(video_each_insert_dir):
                os.makedirs(video_each_insert_dir)
            # 处理视频帧到video_each_insert_dir
            frame_cmd = 'ffmpeg -i {} {}\\frame%04d.png'.format(video_path, video_each_insert_dir)
            os.system(frame_cmd)
            # 获取视频分辨率
            width, height = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_WIDTH), cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_HEIGHT)
            # 排序画面帧
            frame_files = sorted(os.listdir(video_each_insert_dir))

            for i, frame_file in enumerate(frame_files[::frame_insert_num], start=1):
                # 底片原始图片
                frame_files_path = os.path.join(video_each_insert_dir, frame_file)
                print("制作插帧的图像，文件保存路径为", frame_files_path)
                image1 = Image.open(frame_files_path).convert("RGBA")
                # 透明素材图片
                random_image = random.choice(image_list)
                random_image_path = os.path.join(image_dir, random_image)
                image2 = Image.open(random_image_path).convert("RGBA")
                image2 = image2.resize((int(width), int(height)))

                # 调整image2的透明度
                image2 = Image.blend(image1, image2, blend_num)
                # 保存融合后的图像
                image2.save(frame_files_path, "PNG")

            # 使用ffmpeg将所有帧重新组合成视频
            os.system('ffmpeg -y -framerate {} -i {}\\frame%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4'.format(fps, video_each_insert_dir))

            # 获取音频时长
            input_audio_duration = get_audio_duration(video_path)
            output_audio_duration = get_audio_duration("output.mp4")

            # 根据音频长度判断是否加速或减速
            if input_audio_duration < output_audio_duration:
                speed_change = input_audio_duration / output_audio_duration
                ffmpeg_speed_command = f'ffmpeg -y -i output.mp4 -filter:v "setpts={speed_change}*PTS" temp.mp4'
                subprocess.run(ffmpeg_speed_command, shell=True)
            else:
                speed_change = output_audio_duration / input_audio_duration
                ffmpeg_speed_command = f'ffmpeg -y -i output.mp4 -filter:v "setpts={speed_change}*PTS" temp.mp4'
                subprocess.run(ffmpeg_speed_command, shell=True)

            # 将原视频的音频合并到新视频中
            output_video_file_path = os.path.join(video_each_dir, "frame_insert.mp4")
            merge_audio_cmd = f"ffmpeg -y -i temp.mp4 -i {video_path} -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -shortest {output_video_file_path}"
            subprocess.run(merge_audio_cmd, shell=True)

            # 删除临时文件
            subprocess.run("del temp.mp4", shell=True)
            subprocess.run("del output.mp4", shell=True)

    print("全部视频处理完毕")


def video_base_add_function():
    result_info = user_authenticate()
    print(result_info["msg"])
    # 图片路径
    # print(MediaDir)
    # print(request)

    if '用户验证通过' in result_info["msg"]:
        # 获取视频设置基础参数
        last_record = FrameProcess.objects.last()
        # 使用values()方法将模型实例转换为字典
        last_record_dict = last_record.__dict__
        # 删除不必要的键 '_state'，它不是模型字段
        del last_record_dict['_state'], last_record_dict['id']

        fps = last_record_dict['fps']
        frame_insert_num = last_record_dict['frame_insert_num']
        blend_num = last_record_dict['blend_num']
        add_min_count = last_record_dict['add_min_count']
        add_max_count = last_record_dict['add_max_count']

        # 获取需要处理的视频列表
        video_dir = os.path.join(BASE_DIR, "VideoProcess", "video", "base")
        video_list = os.listdir(video_dir)

        # 在result下创建项目,批量处理
        for video_file in video_list:
            # 被处理的视频文件路径
            video_path = os.path.join(video_dir, video_file)
            # 数据处理保存文件的目录
            video_each_dir = os.path.join(BASE_DIR, "VideoProcess", "result", video_file)
            if not os.path.exists(video_each_dir):
                os.makedirs(video_each_dir)
            # 创建frame目录
            video_each_add_dir = os.path.join(video_each_dir, "add_frame")
            if not os.path.exists(video_each_add_dir):
                os.makedirs(video_each_add_dir)
            # 处理视频帧到video_each_insert_dir
            frame_cmd = 'ffmpeg -i {} {}\\frame%04d.png'.format(video_path, video_each_add_dir)
            os.system(frame_cmd)
            # 排序画面帧
            frame_files = sorted(os.listdir(video_each_add_dir))

            def copy_and_rename_random_images(source_folder, destination_folder, min_count=add_min_count, max_count=add_max_count):
                image_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

                # 计算要复制的图片数量
                num_images_to_copy = random.randint(min_count, max_count)

                n = 0
                # 随机选择并复制图片
                selected_images = random.sample(image_files, num_images_to_copy)
                for image in selected_images:
                    source_path = os.path.join(source_folder, image)
                    destination_path = os.path.join(destination_folder, f"{image}_copy.png")
                    shutil.copy(source_path, destination_path)
                    n = n + 1
                print("复制出来 {} 帧".format(str(n)))

            # 调用函数进行复制和重命名操作
            copy_and_rename_random_images(video_each_add_dir, video_each_add_dir)

            # 3. 重新命名所有帧以保持连续性
            all_frames = sorted(os.listdir(video_each_add_dir))
            # for idx, frame in enumerate(all_frames, start=1):
            #     os.rename(f'{video_each_add_dir}\\{frame}', f'{video_each_add_dir}/new_frame{idx:04d}.png')

            # 3. 使用ffmpeg将所有帧重新组合成视频
            os.system(f'ffmpeg -y -framerate {fps} -i {video_each_add_dir}\\frame%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4')

            # 获取音频时长
            input_audio_duration = get_audio_duration(video_path)
            output_audio_duration = get_audio_duration("output.mp4")

            # 根据音频长度判断是否加速或减速
            if input_audio_duration < output_audio_duration:
                speed_change = input_audio_duration / output_audio_duration
                ffmpeg_speed_command = f'ffmpeg -y -i output.mp4 -filter:v "setpts={speed_change}*PTS" temp.mp4'
                subprocess.run(ffmpeg_speed_command, shell=True)
            else:
                speed_change = output_audio_duration / input_audio_duration
                ffmpeg_speed_command = f'ffmpeg -y -i output.mp4 -filter:v "setpts={speed_change}*PTS" temp.mp4'
                subprocess.run(ffmpeg_speed_command, shell=True)

            # 将原视频的音频合并到新视频中
            output_video_file_path = os.path.join(video_each_dir, "frame_add.mp4")
            merge_audio_cmd = f"ffmpeg -y -i temp.mp4 -i {video_path} -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -shortest {output_video_file_path}"
            subprocess.run(merge_audio_cmd, shell=True)

            # 删除临时文件
            subprocess.run("del temp.mp4", shell=True)
            subprocess.run("del output.mp4", shell=True)

    print("全部视频处理完毕")


def video_base_random_cut_function():
    result_info = user_authenticate()
    print(result_info["msg"])
    # 图片路径
    # print(MediaDir)
    # print(request)

    if '用户验证通过' in result_info["msg"]:
        # 获取视频设置基础参数
        last_record = PythonEnv.objects.last()
        # 使用values()方法将模型实例转换为字典
        last_record_dict = last_record.__dict__
        # 删除不必要的键 '_state'，它不是模型字段
        del last_record_dict['_state'], last_record_dict['id']

        python_env_path = last_record_dict['python_env_path']

        # 获取需要处理的视频列表
        video_dir = os.path.join(BASE_DIR, "VideoProcess", "video", "base")
        video_list = os.listdir(video_dir)

        # 在result下创建项目,批量处理
        for video_file in video_list:
            # 被处理的视频文件路径
            video_path = os.path.join(video_dir, video_file)
            # 数据处理保存文件的目录
            video_each_dir = os.path.join(BASE_DIR, "VideoProcess", "result", video_file)
            if not os.path.exists(video_each_dir):
                os.makedirs(video_each_dir)
            # 创建随机拆分的临时文件目录
            temp_cut_dir = os.path.join(BASE_DIR, "VideoProcess", "result", video_file, "temp_cut")
            if not os.path.exists(temp_cut_dir):
                os.makedirs(temp_cut_dir)
            # 执行按场景拆分
            scenedetect_path = os.path.join(python_env_path, 'Scripts', 'scenedetect.exe')
            scenedetect_cmd = "{} -i {} --output {} detect-adaptive split-video".format(scenedetect_path, video_path, temp_cut_dir)
            os.system(scenedetect_cmd)
            # 拼接视频重新排序随机
            video_list = [os.path.join(temp_cut_dir, f) for f in os.listdir(temp_cut_dir) if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]  # 你可以根据需要添加更多的视频格式
            random.shuffle(video_list)  # 随机排序视频文件
            # 生成视频文件路径列表文件
            with open('video_list.txt', 'w') as f:
                for video in video_list:
                    f.write(f"file '{video}'\n")
            # 使用ffmpeg拼接视频
            output_concatenated_temp_path = os.path.join(video_each_dir, "output_concatenated_temp.mp4")
            output_concatenated_path = os.path.join(video_each_dir, "output_concatenated.mp4")
            os.system("ffmpeg -y -f concat -safe 0 -i video_list.txt -c copy {}".format(output_concatenated_temp_path))
            # 替换音频
            os.system("ffmpeg -y -i {} -i {} -c:v copy -c:a aac -strict experimental -map 0:v -map 1:a -y {}".format(output_concatenated_temp_path, video_path,
                                                                                                                     output_concatenated_path))
            # 删除临时的视频列表文件
            os.remove('video_list.txt')
            subprocess.run("del {}".format(output_concatenated_temp_path), shell=True)

    print("全部视频处理完毕")

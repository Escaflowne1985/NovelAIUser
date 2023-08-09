# # -*- coding: UTF-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class VideoBaseSetting(models.Model):
    fps = models.IntegerField(
        default=25,
        validators=[
            MinValueValidator(20, message='帧率不能低于20'),
            MaxValueValidator(120, message='帧率不能高于120')
        ],
        verbose_name="通用帧率", help_text="范围 20 到 120 之间"
    )
    brightness_num = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(-1.0, message='亮度不能低于-1.0'),
            MaxValueValidator(1.0, message='亮度不能高于1.0')
        ],
        verbose_name="通用亮度", help_text="范围 -1 到 1 之间"
    )
    saturation_num = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0, message='亮度不能低于0'),
            MaxValueValidator(3, message='亮度不能高于3.0')
        ],
        verbose_name="通用饱和度", help_text="范围 0 到 3.0 之间"
    )
    contrast_num = models.FloatField(
        default=1.0,
        validators=[
            MinValueValidator(-2.0, message='亮度不能低于-2.0'),
            MaxValueValidator(2.0, message='亮度不能高于2.0')
        ],
        verbose_name="通用对比度度", help_text="范围 -2 到 2 之间"
    )

    unsharp_l_msize_x = models.IntegerField(
        default=5,
        validators=[
            MinValueValidator(3, message='亮度不能低于3'),
            MaxValueValidator(10, message='亮度不能高于10')
        ],
        verbose_name="X方向的锐化半径", help_text="范围 3 到 10 之间"
    )
    unsharp_l_msize_y = models.IntegerField(
        default=5,
        validators=[
            MinValueValidator(3, message='亮度不能低于3'),
            MaxValueValidator(10, message='亮度不能高于10')
        ],
        verbose_name="Y方向的锐化半径", help_text="范围 3 到 10 之间"
    )
    unsharp_l_amount = models.IntegerField(
        default=5,
        validators=[
            MinValueValidator(-2, message='亮度不能低于-2'),
            MaxValueValidator(5, message='亮度不能高于5')
        ],
        verbose_name="锐化强度", help_text="范围 -2 到 5 之间"
    )

    hqdn3d_luma_spatial = models.FloatField(
        default=1.5,
        verbose_name="空间降噪强度", help_text="较大的值会增加降噪效果"
    )
    hqdn3d_chroma_spatia = models.FloatField(
        default=1.5,
        verbose_name="色度通道降噪强度", help_text="较大的值会增加降噪效果"
    )
    hqdn3d_luma_tmp = models.IntegerField(
        default=6,
        verbose_name="时间降噪强度", help_text="较大的值会增加降噪效果"
    )
    hqdn3d_chroma_tmp = models.IntegerField(
        default=6,
        verbose_name="色度时间降噪强度", help_text="较大的值会增加降噪效果"
    )

    scale = models.CharField(
        max_length=20, default="",
        choices=(
            ("480P", "480P(横版)"),
            ("720P", "720P(横版)"),
            ("1080P", "1080P(横版)"),
            ("横竖互换", "横竖互换"),
            ("自定义", "自定义"),
        ),
        verbose_name="视频分辨率"
    )

    scale_x = models.IntegerField(
        default=100,
        verbose_name="自定义分辨率宽", help_text="只有视频分辨率选择自定义才会生效"
    )
    scale_y = models.IntegerField(
        default=100,
        verbose_name="自定义分辨率宽", help_text="只有视频分辨率选择自定义才会生效"
    )

    transpose = models.CharField(
        max_length=20, default="",
        choices=(
            ("逆时针旋转90度", "逆时针旋转90度"),
            ("顺时针旋转90度", "顺时针旋转90度"),
            ("水平旋转", "水平旋转"),
            ("垂直旋转", "垂直旋转"),
            ("不操作", "不操作"),
        ),
        verbose_name="视频旋转"
    )
    frame_set = models.CharField(
        max_length=20, default="",
        choices=(
            ("设置抽帧", "设置抽帧"),
            ("不设置抽帧", "不设置抽帧"),
        ),
        verbose_name="抽帧设置"
    )
    frame_set_min = models.IntegerField(
        default=20,
        verbose_name="随机抽帧下限", help_text="抽帧在【下限-上限】之间随机抽帧"
    )
    frame_set_max = models.IntegerField(
        default=30,
        verbose_name="随机抽帧上限", help_text="抽帧在【下限-上限】之间随机抽帧"
    )

    class Meta:
        verbose_name = "视频基本设置"
        verbose_name_plural = verbose_name


class FrameProcess(models.Model):
    fps = models.IntegerField(
        default=30,
        validators=[
            MinValueValidator(20, message='帧率不能低于20'),
            MaxValueValidator(120, message='帧率不能高于120')
        ],
        verbose_name="通用帧率", help_text="范围 20 到 120 之间"
    )
    frame_insert_num = models.IntegerField(
        default=25,
        verbose_name="间隔插入帧数", help_text="推荐 20 到 30 之间"
    )
    blend_num = models.FloatField(
        default=0.01,
        verbose_name="帧透明度", help_text="0 到 1 之间，0表示全透明，1表示原图"
    )

    add_min_count = models.IntegerField(
        default=20,
        verbose_name="随机抽帧下限", help_text="抽帧在【下限-上限】之间随机补帧"
    )
    add_max_count = models.IntegerField(
        default=30,
        verbose_name="随机抽帧上限", help_text="抽帧在【下限-上限】之间随机补帧"
    )

    class Meta:
        verbose_name = "插帧/补帧设置"
        verbose_name_plural = verbose_name

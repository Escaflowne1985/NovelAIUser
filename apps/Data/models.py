from django.db import models
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete
from NovelAIUser.settings import *
import shutil


# 文生图部分

class Task(models.Model):
    story_framework = models.TextField(
        default="-",
        verbose_name="故事框架", help_text="如果没有可以不填"
    )
    content = models.TextField(
        verbose_name="故事正文", help_text="文章整理过之后直接复制过来接口"
    )
    len_text = models.IntegerField(
        verbose_name="文章字数计算", blank=True
    )
    type = models.CharField(
        max_length=50,
        verbose_name="文章类别", help_text="类别相同会将所有同类文章放到此目录下"
    )
    en_name = models.CharField(
        max_length=50,
        verbose_name="文章英文名", help_text="故事正文下所有的数据都会在次目录下保存"
    )
    cn_name = models.CharField(
        max_length=50,
        verbose_name="文章中文名", help_text="生成数据文件视频和docx的命名"
    )
    status = models.CharField(
        max_length=5, choices=(("已完成", "已完成"), ("未完成", "未完成")),
        verbose_name="数据状态", help_text="批量执行时会跳过标记已完成的数据"
    )
    lora_temp = models.TextField(
        verbose_name="lora 配置", help_text="不懂尽量不要动", blank=True, null=True
    )
    content_start = models.CharField(
        max_length=200, default="###", blank=True, null=True,
        verbose_name="开头文案", help_text="黄金5秒开头文案"
    )
    content_start_json = models.TextField(
        default="", blank=True, null=True,
        verbose_name="开头文案", help_text="黄金5秒开头文案json"
    )

    class Meta:
        verbose_name = "文生图任务管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}/{}/{}'.format(self.type, self.en_name, self.cn_name)


class TaskEach(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    txt = models.TextField(verbose_name="每句话的文章正文")
    index = models.CharField(max_length=255, verbose_name="每句话的文章索引")
    prompt = models.TextField(verbose_name="每句话的文章正面词")
    negative = models.TextField(verbose_name="每句话的文章负面此")
    img = models.CharField(max_length=255, verbose_name="每句话图片保存地址")
    ts = models.CharField(max_length=255, verbose_name="ts时间戳", help_text="Claud API使用")

    class Meta:
        verbose_name = "文章明细管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.txt


@receiver(post_delete, sender=Task)
def create_folder_after_delete(sender, instance, **kwargs):
    # print(instance.type, instance.en_name)
    dir_name = os.path.join(BASE_DIR, "Txt2Video", instance.type, instance.en_name)
    # print(dir_name)
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

from django.db import models
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete
from NovelAIUser.settings import *
import shutil


# 文生图部分

class MovieTask(models.Model):
    type = models.CharField(
        max_length=50,
        verbose_name="电影类别", help_text="类别相同会将所有同类文章放到此目录下"
    )
    en_name = models.CharField(
        max_length=50,
        verbose_name="视频英文名", help_text="请将处理好的视频仍在 MovieProcess/base 文件夹下，不能有中文"
    )
    cn_name = models.CharField(
        max_length=50,
        verbose_name="视频中文名", help_text="最后生成 MovieProcess/result 文件夹下找对应的内容"
    )
    status = models.CharField(
        max_length=5, choices=(("已完成", "已完成"), ("未完成", "未完成")),
        verbose_name="数据状态", help_text="批量执行时会跳过标记已完成的数据"
    )

    class Meta:
        verbose_name = "影视解说项目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}/{}/{}'.format(self.type, self.en_name, self.cn_name)


class MovieTaskEach(models.Model):
    task = models.ForeignKey(MovieTask, on_delete=models.CASCADE, related_name="MovieTaskEach")
    index = models.CharField(max_length=255, verbose_name="每句话的文章索引")
    txt = models.TextField(verbose_name="每句话的文章正文")
    txt_new = models.TextField(verbose_name="洗稿后的每句话解说")
    start_time = models.CharField(max_length=50, default=" ", verbose_name="字幕开始时间")
    end_time = models.CharField(max_length=50, default=" ", verbose_name="字幕结束时间")

    class Meta:
        verbose_name = "电影解说明细"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.txt


@receiver(post_delete, sender=MovieTask)
def create_folder_after_delete(sender, instance, **kwargs):
    # print(instance.type, instance.en_name)
    dir_name = os.path.join(BASE_DIR, "MovieProcess", instance.type, instance.en_name)
    # print(dir_name)
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

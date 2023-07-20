from django.contrib import admin
import xadmin
from .models import *
from xadmin.layout import *


# Register your models here.

class TaskEachList(object):
    model = TaskEach
    extra = 0
    style = 'accordion'


class TaskAdmin(object):
    list_display = ['status', 'type', 'en_name', 'cn_name', 'len_text']
    show_bookmarks = False
    inlines = [TaskEachList]

    def save_models(self):
        obj = self.new_obj
        obj.len_text = len(obj.content)
        # 数据保存
        obj.save()

    # 设计后台编辑样式
    def get_form_layout(self):
        if self.org_obj is None:
            self.form_layout = (
                Fieldset('状态', 'status'),
                Fieldset('文章info', Row('type', 'len_text'), Row('en_name', 'cn_name')),
                Fieldset('Lora配置', 'lora_temp'),
                Fieldset('开头文案', 'content_start'),
                Fieldset('文章detail', 'story_framework', 'content'),
                Fieldset(None, 'content_start_json', **{"style": "display:None"}),
            )
        else:
            self.form_layout = (
                Fieldset('状态', 'status'),
                Fieldset('文章info', Row('type', 'len_text'), Row('en_name', 'cn_name')),
                Fieldset('Lora配置', 'lora_temp'),
                Fieldset('开头文案', 'content_start'),
                Fieldset('文章detail', 'story_framework', 'content'),
                Fieldset(None, 'content_start_json', **{"style": "display:None"}),
            )
        return super(TaskAdmin, self).get_form_layout()


xadmin.site.register(Task, TaskAdmin)  # 全局设置加载

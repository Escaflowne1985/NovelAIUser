from django.contrib import admin
import xadmin
from .models import *
from xadmin.layout import *


# Register your models here.

class MovieTaskList(object):
    model = MovieTaskEach
    extra = 0
    style = 'accordion'


class MovieTaskAdmin(object):
    list_display = ['status', 'type', 'en_name', 'cn_name']
    show_bookmarks = False
    inlines = [MovieTaskList]

    # 设计后台编辑样式
    def get_form_layout(self):
        if self.org_obj is None:
            self.form_layout = (
                Fieldset('状态', 'status'),
                Fieldset('文章info', Row('type'), Row('en_name', 'cn_name')),
            )
        else:
            self.form_layout = (
                Fieldset('状态', 'status'),
                Fieldset('文章info', Row('type'), Row('en_name', 'cn_name')),
            )
        return super(MovieTaskAdmin, self).get_form_layout()


xadmin.site.register(MovieTask, MovieTaskAdmin)  # 全局设置加载

#coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '编辑界面实现二级联动'

import xadmin
from xadmin.views import BaseAdminPlugin
from xadmin.views.detail import DetailAdminView
from xadmin.views.edit import CreateAdminView
"""
    此插件用于实现二级联动查询
"""

class LinkageFilter(BaseAdminPlugin):
    is_execute = False

    def init_request(self, *args, **kwargs):
        return bool(self.is_execute)

    def get_context(self, context):
        return context

    def get_media(self, media):
        path = self.request.get_full_path()
        current_uri = '{scheme}://{host}'.format(scheme=self.request.scheme, host=self.request.get_host())

        if "add" in path or "update" in path:
            media = media + self.vendor('xadmin.self.select.js')
        return media


xadmin.site.register_plugin(LinkageFilter,CreateAdminView)
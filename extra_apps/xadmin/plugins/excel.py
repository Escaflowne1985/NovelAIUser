# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = ''

from django.template import loader
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView


# excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html',
                                             context=get_context_dict(context)))


site.register_plugin(ListImportExcelPlugin, ListAdminView)

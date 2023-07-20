import xadmin
from Data.models import *
from .models import *
from xadmin.layout import *
from xadmin import views


# Register your models here.

# Adminx 全局设置
class BaseSetting(object):
    # 启用后台主题
    enable_themes = True
    # 切换主题模式
    use_bootswatch = True


# xadmin后台菜单设置
class GlobalSettings(object):
    # 设置站点标题
    site_title = "NovelAI本地后台"
    # 设置站点的页脚
    site_footer = "Mr数据杨制作"
    # 设置默认导航菜单折叠
    menu_style = "accordion"

    def get_site_menu(self):
        DataMenu = {'title': '内容管理', 'menus': (
            {'title': '文章数据', 'icon': 'fa fa-user-o', 'url': self.get_model_url(Task, 'changelist')},
            {'title': 'Lora管理', 'icon': 'fa fa-user-o', 'url': self.get_model_url(LoraModels, 'changelist')},
        )}
        UserMenu = {'title': '数据管理', 'menus': (
            {'title': '验证信息', 'icon': 'fa fa-user-o', 'url': self.get_model_url(UserInfo, 'changelist')},
            {'title': 'GPT_知数云', 'icon': 'fa fa-user-o', 'url': self.get_model_url(GPT_ZSY, 'changelist')},
            {'title': 'GPT_OPENAI', 'icon': 'fa fa-user-o', 'url': self.get_model_url(GPT_OPENAI, 'changelist')},
            {'title': 'GPT_CLOSEAI', 'icon': 'fa fa-user-o', 'url': self.get_model_url(GPT_CLOSEAI, 'changelist')},
            {'title': 'GPT_MICROSOFT', 'icon': 'fa fa-user-o', 'url': self.get_model_url(GPT_MICROSOFT, 'changelist')},
            {'title': 'TTS_MICROSOFT', 'icon': 'fa fa-user-o', 'url': self.get_model_url(TTS_MICROSOFT, 'changelist')},
        )}

        return (DataMenu, UserMenu)


class LoraModelsAdmin(object):
    list_display = ['lora_cn_name', 'lora_en_name']
    show_bookmarks = False


class UserInfoAdmin(object):
    list_display = ['username', 'password']
    show_bookmarks = False


class GPT_ZSYAdmin(object):
    list_display = ['api_key']
    show_bookmarks = False


class GPT_OPENAIAdmin(object):
    list_display = ['api_key']
    show_bookmarks = False


class GPT_CLOSEAIAdmin(object):
    list_display = ['api_key']
    show_bookmarks = False


class GPT_MICROSOFTAdmin(object):
    list_display = ['api_key']
    show_bookmarks = False


class TTS_MICROSOFTAdmin(object):
    list_display = ['api_key']
    show_bookmarks = False


xadmin.site.register(views.CommAdminView, GlobalSettings)  # 全局设置加载
xadmin.site.register(views.BaseAdminView, BaseSetting)  # 注册主体风格切换
xadmin.site.register(LoraModels, LoraModelsAdmin)
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(GPT_ZSY, GPT_ZSYAdmin)
xadmin.site.register(GPT_OPENAI, GPT_OPENAIAdmin)
xadmin.site.register(GPT_CLOSEAI, GPT_CLOSEAIAdmin)
xadmin.site.register(GPT_MICROSOFT, GPT_MICROSOFTAdmin)
xadmin.site.register(TTS_MICROSOFT, TTS_MICROSOFTAdmin)

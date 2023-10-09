import xadmin
from Data.models import *
from .models import *
from Data1.models import *
from Data2.models import *
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
        UserMenu = {'title': '配置管理', 'menus': (
            {'title': '用户验证信息', 'icon': 'fa fa-user-o', 'url': self.get_model_url(UserInfo, 'changelist')},
            {'title': '系统环境路径', 'icon': 'fa fa-user-o', 'url': self.get_model_url(PythonEnv, 'changelist')},
        )}
        ChatGPTMenu = {'title': 'ChatGPT 配置', 'menus': (
            {'title': 'ChatGPT信息', 'icon': 'fa fa-user-o', 'url': self.get_model_url(ChatGPT, 'changelist')},
            {'title': 'GPT_知数云', 'icon': 'fa fa-user-o', 'url': self.get_model_url(GPT_ZSY, 'changelist')},
            {'title': 'GPT_OPENAI', 'icon': 'fa fa-user-o', 'url': self.get_model_url(GPT_OPENAI, 'changelist')},
            {'title': 'GPT_CLOSEAI', 'icon': 'fa fa-user-o', 'url': self.get_model_url(GPT_CLOSEAI, 'changelist')},
            {'title': 'GPT_微软', 'icon': 'fa fa-user-o', 'url': self.get_model_url(GPT_MICROSOFT, 'changelist')},
        )}
        AudioMenu = {'title': '文本转语音 配置', 'menus': (
            {'title': 'TTS_微软', 'icon': 'fa fa-user-o', 'url': self.get_model_url(TTS_MICROSOFT, 'changelist')},
        )}
        StableDiffusionMenu = {'title': 'SD 配置', 'menus': (
            {'title': 'SD环境配置', 'icon': 'fa fa-user-o', 'url': self.get_model_url(StableDiffusion, 'changelist')},
            {'title': 'Lora管理', 'icon': 'fa fa-user-o', 'url': self.get_model_url(LoraModels, 'changelist')},
        )}
        JianYingMenu = {'title': '剪映 配置', 'menus': (
            {'title': '剪映配置', 'icon': 'fa fa-user-o', 'url': self.get_model_url(JianYing, 'changelist')},
        )}

        DataMenu = {'title': '漫剪内容管理', 'menus': (
            {'title': '文章数据', 'icon': 'fa fa-user-o', 'url': self.get_model_url(Task, 'changelist')},

        )}
        Data2Menu = {'title': '影视内容管理', 'menus': (
            {'title': '视频数据', 'icon': 'fa fa-user-o', 'url': self.get_model_url(MovieTask, 'changelist')},
        )}

        UserMenu1 = {'title': '视频处理', 'menus': (
            {'title': '基本处理配置', 'icon': 'fa fa-user-o', 'url': self.get_model_url(VideoBaseSetting, 'changelist')},
            {'title': '插帧/补帧设置', 'icon': 'fa fa-user-o', 'url': self.get_model_url(FrameProcess, 'changelist')},

        )}

        return (UserMenu, ChatGPTMenu, AudioMenu, StableDiffusionMenu, JianYingMenu, DataMenu, Data2Menu, UserMenu1)


# 用户和基础环境
class UserInfoAdmin(object):
    list_display = ['username', 'password']
    show_bookmarks = False


class PythonEnvAdmin(object):
    list_display = ['python_env_path', 'whisper_model']
    show_bookmarks = False


# GPT 功能设置
class ChatGPTAdmin(object):
    list_display = ['api_url', 'questions_gpt', 'max_retries', 'retry_time']
    show_bookmarks = False

    def instance_forms(self):
        super().instance_forms()
        self.form_layout = (
            Fieldset('API调用', 'api_url', Row('max_retries', 'retry_time')),
            Fieldset('GPT提问方式', 'questions_gpt', 'questions_txt_1', 'questions_txt_2'),
        )


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
    list_display = ['speech_gender', 'speech_name', 'speech_style', 'speech_role', 'audio_rate']
    readonly_fields = ['access_token_host', ]
    show_bookmarks = False

    # 自动填充登录账号的ID，设计后台编辑样式
    def instance_forms(self):
        super().instance_forms()
        self.form_layout = (
            Fieldset('API信息', 'api_key', 'access_token_host'),
            Fieldset('发音配置', 'speech_gender', 'speech_name', 'speech_style', 'speech_role', 'audio_rate'),
        )


# Stable Diffusion 绘画设置
class StableDiffusionAdmin(object):
    list_display = ['sd_url', 'lora_describe_choose', 'camera_direction_choose', 'filming_method_choose', ]
    show_bookmarks = False

    # 自动填充登录账号的ID，设计后台编辑样式
    def instance_forms(self):
        super().instance_forms()
        self.form_layout = (
            Fieldset('关键词', 'prompt', 'negative'),
            Fieldset('基础配置',
                     'sd_url',
                     Row('steps', 'sd_sampler'),
                     Row('sd_image_width', 'sd_image_height'),
                     Row('cfg_scale', 'seed')),
            Fieldset('画面修正', 'restore_faces', 'adetailer'),
            Fieldset('高清修复',
                     'enable_hr',
                     Row('hr_upscaler', 'hr_scale'),
                     Row('hr_resize_factor', 'denoising_strength')),
            Fieldset('关键词辅助',
                     Row('lora_describe_choose', 'lora_describe_num'),
                     Row('author_style_str', 'author_style_num'),
                     Row('model_choose_str', 'model_choose_num'),
                     Row('time_backgroud_str', 'time_backgroud_num'),
                     Row('camera_direction_choose', 'camera_direction_str'),
                     'camera_direction_num',
                     Row('filming_method_choose', 'filming_method_str'),
                     'filming_method_num',
                     Row('composition_method_str', 'composition_method_num'),
                     'picture_atmosphere_num', 'sense_speed_num'),
            Fieldset('其他配置', 'nsfw'),
        )


class LoraModelsAdmin(object):
    list_display = ['lora_cn_name', 'lora_en_name']
    show_bookmarks = False


# 剪映配置
class JianYingAdmin(object):
    list_display = ['path', 'image_speed', 'keyframe_direction']
    show_bookmarks = False

    # 自动填充登录账号的ID，设计后台编辑样式
    def instance_forms(self):
        super().instance_forms()
        self.form_layout = (
            Fieldset('配置文件路径配置', 'path'),
            Fieldset('关键帧配置', 'image_speed', 'keyframe_direction'),
        )


xadmin.site.register(views.CommAdminView, GlobalSettings)  # 全局设置加载
xadmin.site.register(views.BaseAdminView, BaseSetting)  # 注册主体风格切换
xadmin.site.register(LoraModels, LoraModelsAdmin)
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(GPT_ZSY, GPT_ZSYAdmin)
xadmin.site.register(GPT_OPENAI, GPT_OPENAIAdmin)
xadmin.site.register(GPT_CLOSEAI, GPT_CLOSEAIAdmin)
xadmin.site.register(GPT_MICROSOFT, GPT_MICROSOFTAdmin)
xadmin.site.register(TTS_MICROSOFT, TTS_MICROSOFTAdmin)
xadmin.site.register(PythonEnv, PythonEnvAdmin)
xadmin.site.register(ChatGPT, ChatGPTAdmin)
xadmin.site.register(StableDiffusion, StableDiffusionAdmin)
xadmin.site.register(JianYing, JianYingAdmin)

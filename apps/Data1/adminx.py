from django.contrib import admin
import xadmin
from .models import *
from xadmin.layout import *


class VideoBaseSettingAdmin(object):
    list_display = ['fps', 'scale', 'frame_set']
    show_bookmarks = False

    # 设计后台编辑样式
    def get_form_layout(self):
        if self.org_obj is None:
            self.form_layout = (
                Fieldset('帧率设置', 'fps'),
                Fieldset('画面设置', Row('brightness_num', 'saturation_num', 'contrast_num')),
                Fieldset('锐化设置', 'unsharp_l_amount', Row('unsharp_l_msize_x', 'unsharp_l_msize_y')),
                Fieldset('降噪设置', Row('hqdn3d_luma_spatial', 'hqdn3d_chroma_spatia'), Row('hqdn3d_luma_tmp', 'hqdn3d_chroma_tmp')),
                Fieldset('分辨率设置', 'scale', 'transpose'),
                Fieldset('抽帧设置', 'frame_set', Row('frame_set_max', 'frame_set_min')),
                # Fieldset(None, 'content_start_json', **{"style": "display:None"}),
            )
        else:
            self.form_layout = (
                Fieldset('帧率设置', 'fps'),
                Fieldset('画面设置', Row('brightness_num', 'saturation_num', 'contrast_num')),
                Fieldset('锐化设置', 'unsharp_l_amount', Row('unsharp_l_msize_x', 'unsharp_l_msize_y')),
                Fieldset('降噪设置', Row('hqdn3d_luma_spatial', 'hqdn3d_chroma_spatia'), Row('hqdn3d_luma_tmp', 'hqdn3d_chroma_tmp')),
                Fieldset('分辨率设置', 'scale', 'transpose'),
                Fieldset('抽帧设置', 'frame_set', Row('frame_set_max', 'frame_set_min')),
                # Fieldset(None, 'content_start_json', **{"style": "display:None"}),
            )
        return super(VideoBaseSettingAdmin, self).get_form_layout()


class FrameProcessAdmin(object):
    list_display = ['fps', 'frame_insert_num', 'blend_num', 'add_min_count', 'add_max_count']
    show_bookmarks = False

    # 设计后台编辑样式
    def get_form_layout(self):
        if self.org_obj is None:
            self.form_layout = (
                Fieldset('帧率设置', 'fps'),
                Fieldset('插帧设置', 'frame_insert_num', 'blend_num', 'contrast_num'),
                Fieldset('补帧设置', 'add_min_count', 'add_max_count'),
            )
        else:
            self.form_layout = (
                Fieldset('帧率设置', 'fps'),
                Fieldset('插帧设置', 'frame_insert_num', 'blend_num', 'contrast_num'),
                Fieldset('补帧设置', 'add_min_count', 'add_max_count'),
            )
        return super(FrameProcessAdmin, self).get_form_layout()


xadmin.site.register(VideoBaseSetting, VideoBaseSettingAdmin)
xadmin.site.register(FrameProcess, FrameProcessAdmin)

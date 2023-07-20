from django.db import models


class LoraModels(models.Model):
    lora_cn_name = models.CharField(
        max_length=100,
        verbose_name="Lora 中文备注", help_text="Lora的文件名称，确保你是SD/models/Lora中有该文件"
    )
    lora_en_name = models.CharField(
        max_length=100, default="<lora:20d_v10:1>",
        verbose_name="Lora SD标签", help_text="你在SD页面选择lora是这样就复制过来这样的内容 <lora:20d_v10:1>"
    )

    class Meta:
        verbose_name = "Lora模型管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}/{}'.format(self.lora_cn_name, self.lora_en_name)


class UserInfo(models.Model):
    username = models.CharField(
        max_length=50,
        verbose_name="验证用户名", help_text="管理员给的，一般是QQ号"
    )
    password = models.CharField(
        max_length=50, default="123456",
        verbose_name="验证密码", help_text="管理员给的，默认123456"
    )

    class Meta:
        verbose_name = "用户基本信息"
        verbose_name_plural = verbose_name


class GPT_ZSY(models.Model):
    api_key = models.CharField(
        max_length=100,
        verbose_name="API秘钥",
        help_text="注册地址：https://auth.zhishuyun.com/auth/login?inviter_id=501cdcee-9887-4837-98a0-580df563add8&redirect=https://data.zhishuyun.com"
    )

    class Meta:
        verbose_name = "知数云 GPT key，一条数据一个"
        verbose_name_plural = verbose_name


class GPT_OPENAI(models.Model):
    api_key = models.CharField(
        max_length=100,
        verbose_name="API秘钥",
        help_text="注册地址：https://openai.com"
    )

    class Meta:
        verbose_name = "OPENAI GPT key，一条数据一个"
        verbose_name_plural = verbose_name


class GPT_CLOSEAI(models.Model):
    api_key = models.CharField(
        max_length=100,
        verbose_name="API秘钥",
        help_text="注册地址：https://console.closeai-asia.com/r/7247"
    )

    class Meta:
        verbose_name = "CLOSEAI  GPT key，一条数据一个"
        verbose_name_plural = verbose_name


class GPT_MICROSOFT(models.Model):
    api_key = models.CharField(
        max_length=100,
        verbose_name="API秘钥",
        help_text="注册地址：https://learn.microsoft.com/zh-cn/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions"
    )

    class Meta:
        verbose_name = "微软 GPT key，一条数据一个"
        verbose_name_plural = verbose_name


class TTS_MICROSOFT(models.Model):
    api_key = models.CharField(
        max_length=100,
        verbose_name="API秘钥",
        help_text="注册地址：https://azure.microsoft.com/zh-cn/products/cognitive-services/text-to-speech/"
    )

    class Meta:
        verbose_name = "微软 文本转语音 key，一条数据一个"
        verbose_name_plural = verbose_name

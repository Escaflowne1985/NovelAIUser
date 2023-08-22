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


# 用户和基础环境
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


class PythonEnv(models.Model):
    python_env_path = models.CharField(
        max_length=255,
        default="这里修改成你 myenv 的路径",
        help_text='例如 H:/MyGitProject/NovelAI/UserEdition/sell_NovelAI_txt2video_web/myenv'
    )
    whisper_model = models.CharField(
        max_length=20, default="large",
        choices=(
            ("large-v2", "large-v2 需要 14 GB"),
            ("large-v1", "large-v1 需要12 GB"),
            ("large", "large 需要 10 GB"),
            ("medium", "medium 需要 5 GB"),
            ("small", "small 需要 2 GB"),
            ("base", "base 需要 1 GB"),
        ),
        verbose_name="语音转文本模型", help_text="根据自己的显存选择"
    )

    class Meta:
        verbose_name = "设置myenv的路径"
        verbose_name_plural = verbose_name


# GPT 功能设置
class ChatGPT(models.Model):
    API_URL = (
        ("https://api.zhishuyun.com/chatgpt?token=", "知数云1"),
        ("https://api2.zhishuyun.com/chatgpt?token=", "知数云2"),
        ("https://openai.com", "OPENAI"),
        ("https://api.closeai-proxy.xyz", "CloseAI"),
        ("https://fanyi.baidu.com", "【Free】百度直译"),
        ("https://api.anthropic.com", "【Pay】Claude"),
        # ("https://claude.ai", "【Free】Claude【暂不可用】"),
    )
    api_url = models.CharField(
        choices=API_URL,
        max_length=255, verbose_name="API-Url",
        help_text="选择翻译API，支持【知数云，OpenAI,CloseAI,Claude,Slack,百度直译】"
    )
    max_retries = models.IntegerField(
        default=999, verbose_name="访问重试次数", help_text="默认999即自动重试999次"
    )
    retry_time = models.IntegerField(
        default=0, verbose_name="访问重试时间（秒）", help_text="默认0为不强制重拾,具体数值即n秒自动重试"
    )
    QuestionGPT = (
        ("自定义组合", "自定义组合"),
        ("关键词描述权重版1", "【镜头分镜】关键词描述权重版1"),
        ("关键词描述权重版2", "【镜头分镜】关键词描述权重版2"),
        ("关键词描述漫画导演版", "【镜头分镜】关键词描述漫画导演版"),
        ("关键词描述故事叙述版", "【镜头分镜】关键词描述故事叙述版"),
        ("语义切割短句版", "【镜头分镜】语义切割短句版"),
        ("语义切割长句版", "【镜头分镜】语义切割长句版"),
        ("都市情景叙述版", "【镜头分镜】都市情景叙述版"),
        ("【电影解说改写】", "【电影解说】文案改写"),
    )
    questions_gpt = models.CharField(
        max_length=10,
        choices=QuestionGPT, verbose_name="提问组合",
        help_text="支持自定义提问"
    )
    questions_txt_1 = models.TextField(
        verbose_name="自定义组合前半部分", default="-", help_text="提问组合选择【自定义组合】生效，格式为【前半+你的描述+后半】"
    )
    questions_txt_2 = models.TextField(
        verbose_name="自定义组合后半部分", default="-", help_text="提问组合选择【自定义组合】生效，格式为【前半+你的描述+后半】"
    )

    class Meta:
        verbose_name = "【ChatGPT】API设置，只能有一条记录"
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


# 文本转语音配置
class TTS_MICROSOFT(models.Model):
    api_key = models.CharField(
        max_length=100,
        verbose_name="API秘钥",
        help_text="注册地址：https://azure.microsoft.com/zh-cn/products/cognitive-services/text-to-speech/",
        blank=True, null=True
    )

    access_token_host = models.CharField(
        default="eastus.api.cognitive.microsoft.com",
        max_length=100, verbose_name="TTS服务地址", help_text="不懂不要乱动"
    )
    SpeechName = (
        ('zh-CN, XiaoxiaoNeural', '晓晓 （女）'),
        ('zh-CN, YunxiNeural', '云希 （男）'),
        ('zh-CN, YunjianNeural', '云建 （男）'),
        ('zh-CN, XiaoyiNeural', '晓毅 （女）'),
        ('zh-CN, YunyangNeural', '云扬 （男）'),
        ('zh-CN, XiaochenNeural', '晓晨 （女）'),
        ('zh-CN, XiaohanNeural', '晓韩 （女）'),
        ('zh-CN, XiaomengNeural', '晓孟 （女）'),
        ('zh-CN, XiaomoNeural', '晓墨 （女）'),
        ('zh-CN, XiaoqiuNeural', '晓邱 （女）'),
        ('zh-CN, XiaoruiNeural', '晓睿 （女）'),
        ('zh-CN, XiaoshuangNeural', '晓双 （女性、儿童）'),
        ('zh-CN, XiaoxuanNeural', '晓萱 （女）'),
        ('zh-CN, XiaoyanNeural', '晓研 （女）'),
        ('zh-CN, XiaoyouNeural', '晓悠 （女性、儿童）'),
        ('zh-CN, XiaozhenNeural', '晓珍 （女）'),
        ('zh-CN, YunfengNeural', '云风 （男）'),
        ('zh-CN, YunhaoNeural', '云浩 （男）'),
        ('zh-CN, YunxiaNeural', '云霞 （男）'),
        ('zh-CN, YunyeNeural', '云叶 （男）'),
        ('zh-CN, YunzeNeural', '云泽 （男）'),
    )
    speech_name = models.CharField(
        choices=SpeechName, default="zh-CN, YunxiNeural", max_length=255, verbose_name="配音发音人"
    )
    SpeechStyle = (
        ('advertisement_upbeat', '兴奋'), ('affectionate', '高音调'), ('angry', '厌恶'), ('customerservice', '热情'),
        ('calm', '冷静'), ('chat', '轻松'), ('cheerful', '愉快'), ('depressed', '忧郁'), ('disgruntled', '轻蔑'),
        ('documentary-narration', '纪录片'), ('embarrassed', '犹豫'), ('empathetic', '关切'), ('envious', '钦佩'),
        ('excited', '希望'), ('fearful', '紧张'), ('friendly', '愉悦'), ('hopeful', '温和'), ('lyrical', '优美'),
        ('narration-professional', '朗读'), ('narration-relaxed', '阅读'), ('newscast', '新闻'), ('newscast-casual', '通用'),
        ('newscast-formal', '权威'), ('poetry-reading', '快节奏'), ('sad', '悲伤'), ('serious', '严肃'), ('shouting', '高声'),
        ('sports_commentary', '赛事'), ('sports_commentary_excited', '精彩'), ('whispering', '柔和'), ('terrified', '疯狂'),
        ('unfriendly', '无情')
    )

    speech_style = models.CharField(
        choices=SpeechStyle, default="friendly", max_length=255, verbose_name="配音语气"
    )
    SpeechRole = (('Girl', '女孩'), ('Boy', '男孩'), ('YoungAdultFemale', '年轻的成年女性'), ('YoungAdultMale', '年轻的成年男性'),
                  ('OlderAdultFemale', '年长的成年女性'), ('OlderAdultMale', '年长的成年男性'), ('SeniorFemale', '年老女性'),
                  ('SeniorMale', '年老男性'))

    speech_role = models.CharField(
        choices=SpeechRole, default="Boy", max_length=255, verbose_name="配音年龄段"
    )
    SpeechGender = (('Male', '男'), ('Female', '女'))
    speech_gender = models.CharField(
        choices=SpeechGender, default="Male", max_length=20, verbose_name="配音性别"
    )
    audio_rate = models.FloatField(
        verbose_name="语速倍数", default="1.2", help_text="填1.4即原始语速加速*1.4"
    )

    class Meta:
        verbose_name = "【微软】文本转语音，只能有一条记录"
        verbose_name_plural = verbose_name


# Stable Diffusion 绘画设置
class StableDiffusion(models.Model):
    prompt = models.TextField(
        verbose_name="正面词前缀", help_text="用于修饰画面用，不需要可以不填,填写lora可以固定角色或风格",
        default="best quality ,masterpiece, illustration, an extremely delicate and beautiful, extremely detailed ,CG ,unity ,8k wallpaper, ",
        blank=True, null=True
    )
    negative = models.TextField(
        verbose_name="负面词", help_text="用于修饰画面用，不需要可以不填",
        default="NSFW,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy,(long hair:1.4),DeepNegative,(fat:1.2),facing away, looking away,tilted head, {Multiple people}, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit, extra arms, extra leg, extra foot,",
        blank=True, null=True
    )
    lora_describe_choose = models.CharField(
        max_length=100, default="自定义",
        choices=(("自定义", "自定义"), ("全自动", "全自动")), verbose_name="人物描述模式", help_text="自行选择"
    )
    lora_describe_num = models.IntegerField(
        default=0, verbose_name="人物描述强度", help_text="只支持正整数倍数，会在全部关键词中生效"
    )

    AuthorStyle = (
        ("不选择", "不选择"),
        ("《黑暗骑士归来》", "《黑暗骑士归来》"),
        ("《超现实疯人院》", "《超现实疯人院》"),
        ("《小林家的龙女仆》", "《小林家的龙女仆》"),
        ("《红翼机器人》", "《红翼机器人》"),
        ("《魔戒》", "《魔戒》"),
        ("《未来战士》", "《未来战士》"),
        ("《Halo 4》", "《Halo 4》"),
        ("《Beck》", "《Beck》"),
        ("《妖怪手表》", "《妖怪手表》"),
        ("《浪客剑心》", "《浪客剑心》"),
        ("《狼的孩子雨和雪》", "《狼的孩子雨和雪》"),
        ("《死神》", "《死神》"),
        ("《你的名字。》", "《你的名字。》"),
        ("《美少女战士》", "《美少女战士》"),
        ("《魔神凯撒》", "《魔神凯撒》"),
        ("《龙珠》", "《龙珠》"),
        ("《阿拉蕾》、《大王小王》", "《阿拉蕾》、《大王小王》"),
        ("《犬夜叉》、《美少女战士》", "《犬夜叉》、《美少女战士》"),
        ("《新世纪福音战士》", "《新世纪福音战士》"),
        ("《AKIRA》", "《AKIRA》"),
        ("《龙猫》、《千与千寻》", "《龙猫》、《千与千寻》"),
        ("《借物少女艾莉緹》", "《借物少女艾莉緹》"),
        ("《千年女优》", "《千年女优》"),
        ("《夜明前的琉璃色》", "《夜明前的琉璃色》"),
        ("《魔女宅急便》", "《魔女宅急便》"),
        ("《声之形》、《春物》", "《声之形》、《春物》"),
        ("《SLAM DUNK》、《Code Geass 反叛的鲁路修》", "《SLAM DUNK》、《Code Geass 反叛的鲁路修》"),
        ("《火影忍者》", "《火影忍者》"),
        ("《白雪公主与七个小矮人》、《小飞象》", "《白雪公主与七个小矮人》、《小飞象》"),
        ("《绵羊出击》系列、《机器鸟历险记》", "《绵羊出击》系列、《机器鸟历险记》"),
        ("《玩具总动员》系列、《海底总动员》", "《玩具总动员》系列、《海底总动员》"),
        ("《暗夜奇遇记》、《魔发奇缘》", "《暗夜奇遇记》、《魔发奇缘》"),
        ("《美女与野兽》、《小鹿斑比》", "《美女与野兽》、《小鹿斑比》"),
        ("《史蒂文·尤妮佩》", "《史蒂文·尤妮佩》"),
        ("《邪恶力量》、《星球大战：克隆人战争》", "《邪恶力量》、《星球大战：克隆人战争》"),
        ("《布兰之谷》、《海洋之歌》", "《布兰之谷》、《海洋之歌》"),
        ("《汤姆猫和杰瑞鼠》", "《汤姆猫和杰瑞鼠》"),
        ("《火垂るの墓》", "《火垂るの墓》"),
        ("《三个老头的疯狂旅程》", "《三个老头的疯狂旅程》"),
        ("《超人总动员》、《无敌破坏王》", "《超人总动员》、《无敌破坏王》"),
        ("《珍爱生命》", "《珍爱生命》"),
        ("《幸福工厂》", "《幸福工厂》"),
        ("《红龙的夏天》", "《红龙的夏天》"),
        ("《疯狂农场》", "《疯狂农场》"),
        ("《胡桃夹子》、《这不是一支烟斗》", "《胡桃夹子》、《这不是一支烟斗》"),
        ("涂鸦艺术《生命之舞》", "涂鸦艺术《生命之舞》")
    )
    author_style_str = models.CharField(
        max_length=100, default="不选择",
        choices=AuthorStyle, verbose_name="作者风格", help_text="自行选择"
    )
    author_style_num = models.IntegerField(
        default=0, verbose_name="作者风格强度", help_text="只支持正整数倍数，会在全部关键词中生效"
    )
    ModelChoose = (
        ('不选择', '不选择'),
        ('漫画模式', '漫画模式随机'),
        ('电影模式', '电影模式随机'),
    )
    model_choose_str = models.CharField(
        max_length=100, default='不选择',
        choices=ModelChoose, verbose_name="分镜模式", help_text="会直接应用到全部画面片段"
    )
    model_choose_num = models.IntegerField(
        default=0, verbose_name="分镜模式强度", help_text="只支持正整数倍数，会在全部关键词中生效"
    )
    TimeBackgroud = (
        ("不选择", "不选择"),
        ("中世纪", "中世纪"),
        ("文艺复兴", "文艺复兴"),
        ("日本明治時代", "日本明治時代"),
        ("工业革命", "工业革命"),
        ("日本江戸時代", "日本江戸時代"),
        ("繁华的二十年代", "繁华的二十年代"),
        ("冷战时期", "冷战时期"),
        ("信息时代", "信息时代"),
        ("中华宋朝", "中华宋朝"),
        ("数字时代", "数字时代"),
        ("中华战国时期", "中华战国时期"),
        ("青铜时代", "青铜时代"),
        ("铁器时代", "铁器时代"),
        ("古典时代", "古典时代"),
        ("维多利亚时代", "维多利亚时代"),
        ("镀金时代", "镀金时代"),
        ("爵士时代", "爵士时代"),
        ("太空时代", "太空时代"),
        ("古埃及", "古埃及"),
        ("好莱坞黄金时代", "好莱坞黄金时代"),
        ("中华唐朝", "中华唐朝"),
        ("后现代主义", "后现代主义"),
        ("平和年代", "平和年代"),
        ("启蒙时代", "启蒙时代"),
        ("哥特式时期", "哥特式时期"),
        ("探险时代", "探险时代"),
        ("中华明朝", "中华明朝"),
        ("原子时代", "原子时代"),
        ("现代主义", "现代主义")
    )
    time_backgroud_str = models.CharField(
        max_length=100, default="不选择",
        choices=TimeBackgroud, verbose_name="时代背景", help_text="自行选择"
    )
    time_backgroud_num = models.IntegerField(
        default=0, verbose_name="时代背景强度", help_text="只支持正整数倍数，会在全部关键词中生效"
    )

    camera_direction_choose = models.CharField(
        max_length=100, default="自定义",
        choices=(("自定义", "自定义"), ("全自动", "全自动")), verbose_name="画面镜头模式", help_text="自行选择，对话多文章建议选全自动"
    )
    CameraDirection = (
        ("不选择", "不选择"),
        ("随机", "随机"),
        ("向左", "向左"),
        ("向右", "向右"),
        ("向上", "向上"),
        ("向下", "向下"),
        ("向前", "向前"),
        ("向后", "向后"),
        ("北方", "北方"),
        ("南方", "南方"),
        ("东方", "东方"),
        ("西方", "西方"),
        ("东北方", "东北方"),
        ("西北方", "西北方"),
        ("东南方", "东南方"),
        ("西南方", "西南方"),
        ("水平的", "水平的"),
        ("垂直的", "垂直的"),
        ("对角线的", "对角线的"),
        ("升序的", "升序的"),
        ("降序的", "降序的"),
        ("顺时针方向的", "顺时针方向的")
    )
    camera_direction_str = models.CharField(
        max_length=100, default="随机",
        choices=CameraDirection, verbose_name="画面镜头", help_text="自行选择"
    )
    camera_direction_num = models.IntegerField(
        default=0, verbose_name="画面镜头强度", help_text="只支持正整数倍数，会在全部关键词中生效"
    )

    filming_method_choose = models.CharField(
        max_length=100, default="自定义",
        choices=(("自定义", "自定义"), ("全自动", "全自动")), verbose_name="拍摄方法模式", help_text="自行选择"
    )
    FilmingMethod = (
        ("不选择", "不选择"), ("随机", "随机"), ("特写镜头", "特写镜头"), ("螃蟹镜头", "螃蟹镜头"), ("地板水平镜头", "地板水平镜头"), ("膝盖水平镜头", "膝盖水平镜头"),
        ("臀部水平镜头", "臀部水平镜头"), ("万花筒镜头", "万花筒镜头"), ("红外线镜头", "红外线镜头"), ("热成像镜头", "热成像镜头"), ("鸟瞰图", "鸟瞰图"),
        ("高角度镜头", "高角度镜头"), ("蚯蚓视角镜头", "蚯蚓视角镜头"), ("上帝视角镜头", "上帝视角镜头"), ("无人机镜头", "无人机镜头"), ("子弹时间镜头", "子弹时间镜头"),
        ("斯诺里卡姆镜头", "斯诺里卡姆镜头"), ("移轴镜头", "移轴镜头"), ("变形镜头", "变形镜头"), ("360度镜头", "360度镜头"), ("空中镜头", "空中镜头"),
        ("望远镜镜头", "望远镜镜头"), ("显微镜镜头", "显微镜镜头"), ("胸部水平镜头", "胸部水平镜头"), ("天空水平镜头", "天空水平镜头"), ("水下镜头", "水下镜头"),
        ("分光镜头", "分光镜头"), ("低调镜头", "低调镜头"), ("高调镜头", "高调镜头"), ("剪影镜头", "剪影镜头"), ("夜视镜头", "夜视镜头"), ("慢动作镜头", "慢动作镜头"),
        ("极端特写镜头", "极端特写镜头"), ("中特写镜头", "中特写镜头"), ("中景镜头", "中景镜头"), ("中长景镜头", "中长景镜头"), ("长景镜头", "长景镜头"),
        ("极长景镜头", "极长景镜头"), ("全景镜头", "全景镜头"), ("牛仔镜头", "牛仔镜头"), ("鸟瞰视角", "鸟瞰视角"), ("蚯蚓视角", "蚯蚓视角"), ("高角度", "高角度"),
        ("低角度", "低角度"), ("荷兰角度", "荷兰角度"), ("正面角度", "正面角度"), ("肩膀后方镜头", "肩膀后方镜头"), ("视角镜头", "视角镜头"), ("两人镜头", "两人镜头"),
        ("三人镜头", "三人镜头"), ("建立镜头", "建立镜头"), ("插曲镜头", "插曲镜头"), ("反应镜头", "反应镜头"), ("插入镜头", "插入镜头"), ("屏幕外镜头", "屏幕外镜头"),
        ("反角度镜头", "反角度镜头"), ("底部镜头", "底部镜头"), ("倾斜镜头", "倾斜镜头"), ("平移镜头", "平移镜头"), ("放大镜头", "放大镜头"), ("缩小镜头", "缩小镜头"),
        ("推进镜头", "推进镜头"), ("拉远镜头", "拉远镜头"), ("跟踪镜头", "跟踪镜头"), ("稳定器镜头", "稳定器镜头"), ("手持镜头", "手持镜头"), ("起重镜头", "起重镜头"),
        ("航拍镜头", "航拍镜头"), ("分屏镜头", "分屏镜头"), ("静帧镜头", "静帧镜头")
    )
    filming_method_str = models.CharField(
        max_length=100, default="随机",
        choices=FilmingMethod, verbose_name="拍摄方法", help_text="自行选择"
    )
    filming_method_num = models.IntegerField(
        default=0, verbose_name="拍摄方法强度", help_text="只支持正整数倍数，会在全部关键词中生效"
    )

    CompositionMethod = (
        ("不选择", "不选择"),
        ("随机", "随机"),
        ("迷人的", "迷人的"),
        ("令人着迷的", "令人着迷的"),
        ("令人神魂颠倒的", "令人神魂颠倒的"),
        ("引人注目的", "引人注目的"),
        ("诱人的", "诱人的"),
        ("阴影的", "阴影的"),
        ("威胁的", "威胁的"),
        ("怪异的", "怪异的"),
        ("难以捉摸的", "难以捉摸的"),
        ("有趣的", "有趣的"),
        ("深思的", "深思的"),
        ("反思的", "反思的"),
        ("唤起情感的", "唤起情感的"),
        ("忧伤的", "忧伤的"),
        ("沉思的", "沉思的"),
        ("平静的", "平静的"),
        ("宁静的", "宁静的"),
        ("骚乱的", "骚乱的"),
        ("狂乱的", "狂乱的"),
        ("令人困惑的", "令人困惑的"),
        ("如梦似幻的", "如梦似幻的"),
        ("神秘的", "神秘的"),
        ("飘渺的", "飘渺的")
    )
    composition_method_str = models.CharField(
        max_length=100, default="随机",
        choices=CompositionMethod, verbose_name="情感氛围", help_text="自行选择"
    )
    composition_method_num = models.IntegerField(
        default=0, verbose_name="情感氛围强度", help_text="只支持正整数倍数，会在全部关键词中生效"
    )

    picture_atmosphere_num = models.IntegerField(
        default=0,
        verbose_name="画面氛围", help_text="0表示不输入风格,大于0是明亮乐观，数值越大漫画风格越强,小于0是恐怖阴暗，数值越小写实风格越强"
    )
    sense_speed_num = models.IntegerField(
        default=0,
        verbose_name="SD动态强度", help_text="0表示没有动态强度变化,数值越大，画面越具有动感，太大角色会崩坏"
    )
    steps = models.IntegerField(
        default=30,
        verbose_name="SD采样步数", help_text="高清修复也会选择同样的结果"
    )
    sd_image_width = models.IntegerField(
        default=512,
        verbose_name="图片宽度", help_text="图片宽度，同样也是视频的宽度"
    )
    sd_image_height = models.IntegerField(
        default=512,
        verbose_name="图片宽度", help_text="图片高度，同样也是视频的高度"
    )
    Sampler = (
        ('Euler a', 'Euler a'),
        ('Euler', "Euler"),
        ('DPM++ 2S a Karras', 'DPM++ 2S a Karras'),
        ('DPM++ 2M Karras', 'DPM++ 2M Karras'),
        ('DPM++ SDE Karras', 'DPM++ SDE Karras'),
        ('UniPC', "UniPC"),
    )
    sd_sampler = models.CharField(
        max_length=100, default="Euler a",
        choices=Sampler, verbose_name="图片采样方法"
    )
    seed = models.IntegerField(
        default=-1,
        verbose_name="随机种子", help_text="-1表示不固定，可以在SD里弄好了复制过来"
    )
    RestoreFaces = (("true", "开启面部修复"), ("false", "关闭面部修复"))
    restore_faces = models.CharField(
        max_length=10, default="true",
        choices=RestoreFaces, verbose_name="面部修复", help_text="默认开启"
    )
    ADetailer = (("true", "开启默认ADetailer修复"), ("false", "开启默认ADetailer修复"))
    adetailer = models.CharField(
        max_length=10, default="false",
        choices=RestoreFaces, verbose_name="ADetailer修复", help_text="默认关闭，ADetailer开启需要有对应插件，具体查看使用文档"
    )
    cfg_scale = models.IntegerField(
        default=7,
        verbose_name="提示词相关性"
    )
    Enable = (
        ('true', '开启图像高清修复'),
        ('false', '关闭图像高清修复')
    )
    enable_hr = models.CharField(
        max_length=30, default="true",
        choices=Enable, verbose_name="高清修复", help_text="默认开启高清修复"
    )
    Upscaler = (
        ('R-ESRGAN 4x+ Anime6B', 'R-ESRGAN 4x+ Anime6B'),
        ('R-ESRGAN 4x+', 'R-ESRGAN 4x+'),
        ('ESRGAN_4x', 'ESRGAN_4x'),
    )
    hr_upscaler = models.CharField(
        max_length=100, default="R-ESRGAN 4x+ Anime6B",
        choices=Upscaler, verbose_name="高清修复方法"
    )

    hr_scale = models.FloatField(
        default=1.5,
        verbose_name="图像放大倍数", help_text="这个和视频分辨率没关系"
    )
    hr_resize_factor = models.FloatField(
        default=1.5,
        verbose_name="高清修复图像倍数", help_text="设置的宽度和高度都会乘这个数值,建议和【分辨率倍数】一致"
    )
    denoising_strength = models.FloatField(
        default=0.7,
        verbose_name="图像放大重绘幅度", help_text="不动啥意思的不要乱动"
    )

    NSFW = (("开启", "开启"), ("关闭", "关闭"))
    nsfw = models.CharField(
        choices=NSFW, default="关闭",
        max_length=50, verbose_name="TF鉴黄程序开关"
    )

    sd_url = models.CharField(
        max_length=100, verbose_name="SD地址",
        default="127.0.0.1:7860", help_text="默认本地，云端用户自己填写你的IP地址"
    )

    class Meta:
        verbose_name = "【SD】参数设置，只能有一条记录"
        verbose_name_plural = verbose_name


# 剪映配置
class JianYing(models.Model):
    path = models.CharField(
        max_length=100,
        verbose_name="剪影等配置路径", help_text="直接复制你的项目路径，例如 H:\\debug_NovelAI_txt2video"
    )
    image_speed = models.IntegerField(
        default=50,
        verbose_name="关键帧移动速度", help_text="1-100,100表示整张图描述时间内全部移动完成，一般选择50即可"
    )
    KeyframeDirection = (
        ("四方向", "四方向"), ("八方向", "八方向"), ("上下方向", "上下方向"), ("左右方向", "左右方向")
    )
    keyframe_direction = models.CharField(
        max_length=100, default="四方向",
        choices=KeyframeDirection, verbose_name="关键帧方向", help_text="自行选择"
    )

    class Meta:
        verbose_name = "【剪映】配置，只能有一条记录"
        verbose_name_plural = verbose_name

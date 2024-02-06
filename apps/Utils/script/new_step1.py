# -*- coding: UTF-8 -*-
from Data.models import *
from Config.models import *
from NovelAIUser.settings import *

try:
    from apps.Utils.script.GeneralTools import *
except:
    from apps.Utils.pyd.GeneralTools import *

try:
    from apps.Utils.script.step2 import *
except:
    from apps.Utils.pyd.step2 import *


# LoRA人物配置
def step_1_lora_fuction(request):
    # 用户数据验证
    result_info = user_authenticate()
    print(result_info["msg"])

    lora_dict = {}
    if '用户验证通过' in result_info["msg"]:
        for i in range(1, 11):
            name = request.POST.get(f'name_{i}')
            if name != "-":
                lora_value = request.POST.get(f'lora_{i}')
                description_value = request.POST.get(f'description_{i}')
                lora_dict[name] = ",".join([str(lora_value), str(description_value)])
                # print(name,lora_value, description_value)

        task_id = request.POST.get('task_id')

        # 使用filter()方法选择要更新的对象集合
        objects = Task.objects.filter(id=task_id)
        # 更新所有选中的对象的属性
        objects.update(lora_temp=lora_dict)

        print_info = [
            "LoRA信息配置成功",
            "LoRA配置数量：{}".format(len(lora_dict) - 1),
            "文章类别：{}".format(objects[0].type),
            "英文名称：{}".format(objects[0].en_name),
            "中文名称：{}".format(objects[0].cn_name),
        ]
        print_with_border(print_info)


# 黄金文案5秒
def step_1_gold_start_fuction(num):
    # 用户数据验证
    result_info = user_authenticate()
    print(result_info["msg"])

    # ChatGPT验证
    chat_gpt_dict = get_chat_gpt_model()
    api_url = chat_gpt_dict['api_url']
    max_retries = chat_gpt_dict['max_retries']
    retry_time = None if chat_gpt_dict['retry_time'] == 0 else chat_gpt_dict['retry_time']
    questions_gpt = questions_gpt_dict[chat_gpt_dict['questions_gpt']]
    # print(chat_gpt_dict)

    if '用户验证通过' in result_info["msg"]:

        # 根据设置的参数获取对应的API秘钥
        domain_model_mapping = {
            "zhishuyun.com": GPT_ZSY,
            "openai.com": GPT_OPENAI,
            "api.closeai-proxy.xyz": GPT_CLOSEAI,
        }

        for domain in domain_model_mapping:
            if domain in api_url:
                model = domain_model_mapping[domain]
                api_key_list = list(model.objects.values_list('api_key', flat=True))
                break

        # 根据文案设置黄金5秒提问
        questions_gpt["question_txt_1"] = ''
        questions_gpt["question_txt_2"] = '\n'

        # 获取文章用的前5000个字
        txt_each = Task.objects.filter(id=num)[0].content[:5000]

        print("使用openai的用户验证成功请抓紧切换代理，这里设置了3秒延迟，任务在3秒后开启。")
        time.sleep(3)

        if "openai.com" in api_url:
            content_start = post_with_retry_gpt35(api_key_list[0], questions_gpt, txt_each, max_retries)
        elif "api.closeai-proxy.xyz" in api_url:
            content_start = post_with_retry_CloseAI(api_key_list[0], questions_gpt, txt_each, max_retries)
        elif "claude.ai" in api_url:
            content_start = post_with_retry_ClaudeAI_Free(questions_gpt, txt_each, max_retries)
        elif "api.anthropic.com" in api_url:
            content_start = post_with_retry_ClaudeAI_Pay(questions_gpt, txt_each, max_retries)
        # print(content_start)

        # 分割字符串,获得列表
        items = content_start.split('\n')
        # 将列表转换为 JSON 并格式化输出
        json_str = json.dumps(items, indent=4)
        Task.objects.filter(id=num).update(content_start_json=json_str)

        data_len_txt = "生成黄金文案条目数：{}".format(len(items))

        print_info = [
            data_len_txt,
        ]

        print_with_border(print_info)

        return json_str

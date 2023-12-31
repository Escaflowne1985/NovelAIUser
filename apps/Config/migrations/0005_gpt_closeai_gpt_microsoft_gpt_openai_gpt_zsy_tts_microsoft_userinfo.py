# Generated by Django 3.0.3 on 2023-07-10 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Config', '0004_auto_20230604_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='GPT_CLOSEAI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(help_text='注册地址：https://console.closeai-asia.com/r/7247', max_length=100, verbose_name='API秘钥')),
            ],
            options={
                'verbose_name': 'CLOSEAI  GPT key，一条数据一个',
                'verbose_name_plural': 'CLOSEAI  GPT key，一条数据一个',
            },
        ),
        migrations.CreateModel(
            name='GPT_MICROSOFT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(help_text='注册地址：https://learn.microsoft.com/zh-cn/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions', max_length=100, verbose_name='API秘钥')),
            ],
            options={
                'verbose_name': '微软 GPT key，一条数据一个',
                'verbose_name_plural': '微软 GPT key，一条数据一个',
            },
        ),
        migrations.CreateModel(
            name='GPT_OPENAI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(help_text='注册地址：https://openai.com', max_length=100, verbose_name='API秘钥')),
            ],
            options={
                'verbose_name': 'OPENAI GPT key，一条数据一个',
                'verbose_name_plural': 'OPENAI GPT key，一条数据一个',
            },
        ),
        migrations.CreateModel(
            name='GPT_ZSY',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(help_text='注册地址：https://auth.zhishuyun.com/auth/login?inviter_id=501cdcee-9887-4837-98a0-580df563add8&redirect=https://data.zhishuyun.com', max_length=100, verbose_name='API秘钥')),
            ],
            options={
                'verbose_name': '知数云 GPT key，一条数据一个',
                'verbose_name_plural': '知数云 GPT key，一条数据一个',
            },
        ),
        migrations.CreateModel(
            name='TTS_MICROSOFT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(help_text='注册地址：https://azure.microsoft.com/zh-cn/products/cognitive-services/text-to-speech/', max_length=100, verbose_name='API秘钥')),
            ],
            options={
                'verbose_name': '微软 文本转语音 key，一条数据一个',
                'verbose_name_plural': '微软 文本转语音 key，一条数据一个',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='管理员给的，一般是QQ号', max_length=50, verbose_name='验证用户名')),
                ('password', models.CharField(default='123456', help_text='管理员给的，默认123456', max_length=50, verbose_name='验证密码')),
            ],
            options={
                'verbose_name': '用户基本信息',
                'verbose_name_plural': '用户基本信息',
            },
        ),
    ]

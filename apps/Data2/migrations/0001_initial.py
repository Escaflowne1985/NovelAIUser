# Generated by Django 3.0.3 on 2023-08-09 17:01

import Data2.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='类别相同会将所有同类文章放到此目录下', max_length=50, verbose_name='电影类别')),
                ('en_name', models.CharField(help_text='故事正文下所有的数据都会在次目录下保存', max_length=50, verbose_name='文章英文名')),
                ('cn_name', models.CharField(help_text='生成数据文件视频和docx的命名', max_length=50, verbose_name='文章中文名')),
                ('status', models.CharField(choices=[('已完成', '已完成'), ('未完成', '未完成')], help_text='批量执行时会跳过标记已完成的数据', max_length=5, verbose_name='数据状态')),
            ],
            options={
                'verbose_name': '影视解说项目',
                'verbose_name_plural': '影视解说项目',
            },
        ),
        migrations.CreateModel(
            name='MovieTaskEach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=255, verbose_name='每句话的文章索引')),
                ('txt', models.TextField(verbose_name='每句话的文章正文')),
                ('txt_new', models.TextField(verbose_name='洗稿后的每句话解说')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Data2.MovieTask')),
            ],
            options={
                'verbose_name': '电影解说明细',
                'verbose_name_plural': '电影解说明细',
            },
        ),
    ]

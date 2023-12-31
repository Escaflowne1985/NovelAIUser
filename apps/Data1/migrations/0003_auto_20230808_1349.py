# Generated by Django 3.0.3 on 2023-08-08 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data1', '0002_auto_20230808_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videobasesetting',
            name='frame_set_max',
            field=models.IntegerField(default=30, help_text='抽帧在【下限-上限】之间随机抽帧', verbose_name='随机抽帧上限'),
        ),
        migrations.AlterField(
            model_name='videobasesetting',
            name='frame_set_min',
            field=models.IntegerField(default=20, help_text='抽帧在【下限-上限】之间随机抽帧', verbose_name='随机抽帧下限'),
        ),
    ]

# Generated by Django 3.0.3 on 2023-10-09 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0008_auto_20230719_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='content_start',
            field=models.CharField(blank=True, default='###', help_text='黄金5秒开头文案', max_length=200, null=True, verbose_name='开头文案'),
        ),
    ]

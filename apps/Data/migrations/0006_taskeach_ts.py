# Generated by Django 3.0.3 on 2023-07-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0005_auto_20230704_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskeach',
            name='ts',
            field=models.CharField(default=' ', help_text='Claud API使用', max_length=255, verbose_name='ts时间戳'),
            preserve_default=False,
        ),
    ]

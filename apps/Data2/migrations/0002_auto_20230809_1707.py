# Generated by Django 3.0.3 on 2023-08-09 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Data2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movietaskeach',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MovieTaskEach', to='Data2.MovieTask'),
        ),
    ]

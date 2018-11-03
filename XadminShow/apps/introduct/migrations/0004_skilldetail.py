# Generated by Django 2.0.5 on 2018-10-17 14:53

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('introduct', '0003_auto_20181016_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', DjangoUeditor.models.UEditorField(default='', verbose_name='技能栈详情')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('introduction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='introduct.Introduct', verbose_name='个人简介')),
            ],
            options={
                'verbose_name': '技能详情',
                'verbose_name_plural': '技能详情',
            },
        ),
    ]
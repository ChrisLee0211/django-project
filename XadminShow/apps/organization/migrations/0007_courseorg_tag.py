# Generated by Django 2.0.5 on 2018-10-07 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='全国知名', max_length=10, verbose_name='机构标签'),
        ),
    ]

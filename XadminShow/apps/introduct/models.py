from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.
class Introduct(models.Model):
    name = models.CharField(max_length=20,verbose_name="姓名")
    desc = models.CharField(max_length = 200,verbose_name='个人简介')
    desc_img =models.ImageField(upload_to="introduct/%Y/%m",verbose_name="简介图",max_length=100)
    about_me = UEditorField(verbose_name='关于我',width=600, height=300,imagePath="introduct/ueditor/", filePath="introduct/ueditor/",default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "个人简介"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class MyProject(models.Model):
    introduction = models.ForeignKey(Introduct,verbose_name='个人简介',on_delete=models.CASCADE)
    name = models.CharField(max_length=20,verbose_name='项目名称')
    img = models.ImageField(upload_to="project/%Y/%m",verbose_name="项目图",max_length=100)
    desc = models.CharField(max_length = 500,verbose_name='项目介绍')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "个人项目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class MySkill(models.Model):
    introduction = models.ForeignKey(Introduct,verbose_name='个人简介',on_delete=models.CASCADE)
    name = models.CharField(max_length=20,verbose_name="技术名称")
    desc = models.CharField(max_length = 200,verbose_name='简单介绍')
    img = models.ImageField(upload_to="skill/%Y/%m",verbose_name="技能图标",max_length=100)

    class Meta:
        verbose_name = "技术栈"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SkillDetail(models.Model):
    introduction = models.ForeignKey(Introduct,verbose_name='个人简介',on_delete=models.CASCADE)
    detail = UEditorField(verbose_name='技能栈详情',width=600, height=300,imagePath="introduct/ueditor/", filePath="introduct/ueditor/",default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "技能详情"
        verbose_name_plural = verbose_name


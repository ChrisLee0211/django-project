#_*_encoding:utf-8_*_
from datetime import datetime

from django.db import models

# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20,verbose_name="城市")
    desc = models.CharField(max_length=200,verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    name = models.CharField(max_length=50,verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    category = models.CharField(max_length=20,verbose_name="机构类别",default="yx",choices=(("pxjg","培训机构"),("yx","英雄高校"),("dx","大学个人")))
    tag = models.CharField(max_length=10,verbose_name="机构标签",default="全国知名")
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo",max_length=100)
    address = models.CharField(max_length=150,verbose_name="机构地址")
    city = models.ForeignKey(CityDict,verbose_name="所在城市",on_delete=models.CASCADE)
    students = models.IntegerField(default=0,verbose_name="学习人数")
    course_nums = models.IntegerField(default=0,verbose_name="课程数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#获取课程机构的教师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def get_all_course(self):
        return self.Course_set.all()[:2]

class Teacher(models.Model):
    Org = models.ForeignKey(CourseOrg,verbose_name="所属机构",on_delete=models.CASCADE)
    name = models.CharField(max_length=50,verbose_name="教师名称")
    work_years = models.IntegerField(default=0,verbose_name="工作年限")
    work_company = models.CharField(max_length=50,verbose_name="就职公司")
    work_position = models.CharField(max_length=50,verbose_name="公司职位")
    points = models.CharField(max_length=50,verbose_name="教学特点")
    image = models.ImageField(upload_to="teacher/%Y/%m",verbose_name="头像",max_length=100,null=True,blank=True)
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()

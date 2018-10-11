#_*_encoding:utf-8_*_
from datetime import datetime


from django.db import models

from organization.models import CourseOrg,Teacher
from DjangoUeditor.models import UEditorField
# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name="课程机构",on_delete=models.CASCADE,null=True,blank =True)
    name = models.CharField(max_length=50, verbose_name="课程名称")
    desc = models.CharField(max_length=300,verbose_name="课程描述")
    detail = UEditorField(verbose_name='课程详情',width=600, height=300,imagePath="course/ueditor/", filePath="course/ueditor/",default='')
    teacher = models.ForeignKey(Teacher,verbose_name="课程讲师",on_delete=models.CASCADE,null=True,blank=True)
    is_banner = models.BooleanField(default=False,verbose_name="是否轮播")
    degree = models.CharField(verbose_name="难度",max_length=2,choices=(("cj","初级"),("zj","中级"),("gj","高级")))
    learn_times = models.IntegerField(default=0,verbose_name="学习时长（分钟数）")
    students = models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏人数")
    image = models.ImageField(upload_to="course/%Y/%m",verbose_name="封面图",max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    category = models.CharField(max_length=50, verbose_name="课程类别",default="后端")
    tag = models.CharField(default='',verbose_name="课程标签",max_length=20)
    youneed_know = models.CharField(max_length=300, verbose_name="课程须知",default="")
    teacher_tell = models.CharField(max_length=300, verbose_name="老师告诉你",default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #获取章节数,lesson_set是反向查询外键，也就是从Course表里查询有多少个外键在Lesson表中
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:3]

    def get_course_lesson(self):
        #获取课程章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name

class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name="课程",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="章节名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name="章节",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="视频名称")
    url = models.CharField(max_length=200,verbose_name="访问地址",default='')
    learn_times = models.IntegerField(default=0,verbose_name="学习时长（分钟数）")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name="课程",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="名称")
    download = models.FileField(max_length=100,upload_to="course/resource/%Y/%m",verbose_name="资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
from .models import Course,Lesson,Video,CourseResource,BannerCourse
from extra_apps import xadmin

class LessonInline(object):
    model = Lesson
    extra = 0

class CourseAdmin(object):
    list_display = ['name','desc','course_org','degree','learn_times','students','fav_nums','click_nums','add_time']
    list_filter =['name','desc','detail','degree','learn_times','students','fav_nums','click_nums','add_time']
    search_fields = ['name','desc','detail','degree','students','fav_nums','click_nums']
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums','click_nums','students']
    inlines = [LessonInline]
    list_editable = ['name']
    refresh_times = [3]
    style_fields = {"detail":"ueditor"}

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

class BannerCourseAdmin(object):
    list_display = ['name','desc','course_org','degree','learn_times','students','fav_nums','click_nums','add_time']
    list_filter =['name','desc','detail','degree','learn_times','students','fav_nums','click_nums','add_time']
    search_fields = ['name','desc','detail','degree','students','fav_nums','click_nums']
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums','click_nums','students']
    inlines = [LessonInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonAdmin(object):
    list_display = ['course','name','add_time']
    list_filter =['course__name','name','add_time']
    search_fields = ['course','name']

class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    list_filter =['lesson','name','add_time']
    search_fields = ['lesson','name']

class CourseResourceAdmin(object):
    list_display = ['course','name','download','add_time']
    list_filter = ['course','name','download','add_time']
    search_fields = ['course','name','download']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)


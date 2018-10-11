from .models import CityDict,CourseOrg,Teacher

from extra_apps import xadmin

class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    list_filter = ['name','desc','add_time']
    search_fields = ['name','desc']
    model_icon = 'fa fa-building'

class CourseOrgAdmin(object):
    list_display = ['name','desc','click_nums','fav_nums','image','address','city','add_time']
    list_filter = ['name','desc','click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name','desc','click_nums','fav_nums','image','address','city']
    model_icon = 'fa fa-sitemap'
    readonly_fields = ['fav_nums','click_nums']

class TeacherAdmin(object):
    list_display = ['Org','name','work_years','work_company','work_position','points','click_nums','fav_nums','add_time']
    list_filter = ['Org','name','work_years','work_company','work_position','points','click_nums','fav_nums','add_time']
    search_fields = ['Org','name','work_years','work_company','work_position','points','click_nums','fav_nums']
    model_icon = 'fa fa-user-md'
    readonly_fields = ['fav_nums','click_nums']

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)

from extra_apps import xadmin

from .models import Introduct,MyProject,MySkill,SkillDetail

class IntroductAdmin(object):
    list_display = ['name','desc','add_time']
    list_filter =['name','desc','add_time']
    search_fields = ['name',]
    style_fields = {"about_me":"ueditor"}

class MyProjectAdmin(object):
    list_display = ['name','desc','add_time']
    list_filter =  ['name','desc','add_time']
    search_fields = ['name']

class MySkillAdmin(object):
    list_display = ['name','desc']
    list_filter =  ['name','desc']
    search_fields = ['name']

class SkillDetailAdmin(object):
    list_display = ['detail','add_time']
    list_filter =  ['detail','add_time']
    style_fields = {"detail":"ueditor"}

xadmin.site.register(Introduct,IntroductAdmin)
xadmin.site.register(MyProject,MyProjectAdmin)
xadmin.site.register(MySkill,MySkillAdmin)
xadmin.site.register(SkillDetail,SkillDetailAdmin)
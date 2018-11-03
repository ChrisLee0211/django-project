from django.shortcuts import render
from django.views.generic import View
from .models import MyProject,MySkill,Introduct,SkillDetail

# Create your views here.
class IntroductView(View):
    def get(self,request):
        my_info = Introduct.objects.all()
        my_project = MyProject.objects.all()
        my_Skill = MySkill.objects.all()
        skill_detail = SkillDetail.objects.all()
        return render(request,'introduction.html',{
            'my_info':my_info,
            'my_Skill':my_Skill,
            'my_project':my_project,
            'skill_detail':skill_detail
        })
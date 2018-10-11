import re
from django import forms
from operation.models import UserAsk

class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    def clean_mobile(self):
        #验证手机号码是否合法
        mobile = self.cleaned_data['mobile']
        re_mobile = "/^1(?:3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8\d|9\d)\d{8}$/"
        check = re.compile(re_mobile)
        if check.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法',code="mobile_invalid")
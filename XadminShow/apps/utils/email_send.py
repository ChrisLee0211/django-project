from random import Random

from django.core.mail import send_mail
from users.models import EmailVerifyRecord

from XadminShow.settings import EMAIL_FROM

def random_str(randomlength = 8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxvzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = len(chars)-1
    random = Random()
    for i  in range(randomlength):
        str += chars[random.randint(0,length)]
    return str

def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(8)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == "register":
        email_title = '用户注册激活链接地址'
        email_body = '请点击下方链接以激活用户：http://127.0.0.1:8000/active/%s' %code

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = '用户重置密码'
        email_body = '请点击下方链接以重置密码：http://127.0.0.1:8000/reset/%s' %code
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = '邮箱修改验证码'
        email_body = '你的邮箱验证码为：%s' %code
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        print (send_status)
        if send_status:
            pass
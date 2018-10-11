# django-project

>这个在线自学资源平台涉及技术栈：python3.6+django2.0+mysql5.5+xadmin2.0

注意：
具体的验证码插件、富文本插件分别借用了github上的captcha和Ueditor（Ueditor因为用的Python2开发，无奈只能自己修改一下源码让它匹配python3了）

源码的前端内容主要是借用了慕学上bobby的页面模板，然后自己对部分JS进行了修改。

后台逻辑完全基于django2.0版本自己开发，原因是。。。django2.1开始不支持mysql5.5了！！！！气死我气死我

网站后台管理页面直接用了xadmin，替代了django自己的admin后台，功能更强大更完善

但目前发现xadmin2.0有个BUG暂时比较致命，在后台进行类orm操作去删除model数据时，必定报错，所以后来只能借助Navicat去删了。后面会持续优化这个网页，争取用其他框架再写一次

效果预览如下：
一、平台主页
![image](https://github.com/ChrisLee0211/django-project/blob/master/index.png)

二、导航栏分页之一：
![image](https://github.com/ChrisLee0211/django-project/blob/master/org.png)

三、后台登录页面：
![image](https://github.com/ChrisLee0211/django-project/blob/master/xadmin-login.png)

四、后台管理页面：
![image](https://github.com/ChrisLee0211/django-project/blob/master/xadmin2.png)

from django.db import models


# Create your models here.
# 班级表
class Classes(models.Model):
    classes_name = models.CharField("班级名", max_length=128, unique=True)

    class Meta:
        verbose_name_plural = u'班级表'


class UserProfile(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.IntegerField("用户类型（1.老师 2.学生）")
    user_name = models.CharField("用户账号", max_length=128, unique=True)
    passwd = models.CharField("密码", max_length=128)
    nick_name = models.CharField("昵称", max_length=128, null=True, blank=True, default="王菲")
    stu_number = models.CharField("学号", max_length=128, null=True, blank=True, unique=True)
    the_name = models.CharField("真实姓名", max_length=128, null=True, blank=True, default="")
    sex = models.CharField("性别", max_length=32, null=True, blank=True, default="")

    class Meta:
        verbose_name_plural = u'学生和老师用户'

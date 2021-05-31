from datetime import datetime

from django.utils import timezone
from django.db import models
from apps.users.models import UserProfile, Classes


# Create your models here.

# 题库
class Subject(models.Model):
    subject_name = models.CharField("题目", max_length=4096)
    subject_class = models.CharField("科目", max_length=64, default="")
    subject_unswer = models.CharField("答案", max_length=4096)
    score = models.CharField("分数", max_length=64)


# 试卷分类表
class TranslateClass(models.Model):
    class_name = models.CharField("试卷标题类名", max_length=128)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField("开始时间", default=datetime.now)
    end_time = models.DateTimeField("结束时间", default=timezone.now, blank=True)


# 试卷题目表
class Translate(models.Model):
    translate_class = models.ForeignKey(TranslateClass, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)


# 学生试卷

# 学生题目
# 查询所有试卷，查看  根据试卷查看所对应的学生+答题卡
class StudentSubject(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    translate_class = models.ForeignKey(TranslateClass, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    subject_answer = models.CharField("学生答案", max_length=4096, default="")
    is_commit = models.IntegerField("是否提交（0否， 1是）", default=-1, blank=True)
    user_score = models.FloatField("用户评分", default=-1)
    auto_score = models.FloatField("自动评分", default=-1)
    is_auto_score = models.IntegerField("自动评分是否确认（0否， 1是）", default=-1)
    is_teacher_score = models.IntegerField("老师是否评分（0否， 1是）", default=-1)

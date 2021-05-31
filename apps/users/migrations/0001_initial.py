# Generated by Django 3.1.7 on 2021-03-27 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes_name', models.CharField(max_length=128, unique=True, verbose_name='班级名')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(verbose_name='用户类型（1.老师 2.学生）')),
                ('user_name', models.CharField(max_length=128, unique=True, verbose_name='用户账号')),
                ('passwd', models.CharField(max_length=128, verbose_name='密码')),
                ('nick_name', models.CharField(blank=True, default=models.CharField(max_length=128, unique=True, verbose_name='用户账号'), max_length=128, null=True, verbose_name='昵称')),
                ('stu_number', models.CharField(blank=True, default='', max_length=128, null=True, unique=True, verbose_name='学号')),
                ('the_name', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='真实姓名')),
                ('sex', models.CharField(blank=True, default='', max_length=32, null=True, verbose_name='性别')),
                ('classes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.classes')),
            ],
        ),
    ]

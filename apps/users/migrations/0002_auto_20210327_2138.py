# Generated by Django 3.1.7 on 2021-03-27 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='stu_number',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True, verbose_name='学号'),
        ),
    ]

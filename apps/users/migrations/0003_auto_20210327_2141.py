# Generated by Django 3.1.7 on 2021-03-27 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210327_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(blank=True, default='test', max_length=128, null=True, verbose_name='昵称'),
        ),
    ]

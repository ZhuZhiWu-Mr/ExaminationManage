# Generated by Django 3.2.3 on 2021-05-22 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210327_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(blank=True, default='王菲', max_length=128, null=True, verbose_name='昵称'),
        ),
    ]

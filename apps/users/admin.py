from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import (
    UserProfile,
    Classes
)


class ClassesAdmin(admin.ModelAdmin):
    list_display = ('classes_name',)
    search_fields = ('classes_name',)


admin.site.register(Classes, ClassesAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'classes_classes_name', 'user_type', 'user_name', 'passwd', 'nick_name', 'stu_number', 'the_name', 'sex'
    )  # list
    search_fields = ('user_name',)

    def classes_classes_name(self, obj):
        if obj and obj.classes:
            return obj.classes.classes_name
        return obj.classes

    classes_classes_name.short_description = '班级名'


admin.site.register(UserProfile, UserProfileAdmin)

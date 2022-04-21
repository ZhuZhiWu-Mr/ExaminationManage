from django.contrib import admin

# Register your models here.
from .models import (
    Subject,
    TranslateClass
)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'subject_class', 'subject_unswer', 'score', 'type')  # list
    search_fields = ('subject_name',)


admin.site.register(Subject, SubjectAdmin)


class TranslateClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'classes_classes_name', 'start_time', 'end_time')  # list
    search_fields = ('classes_classes_name',)

    def classes_classes_name(self, obj):
        if obj and obj.classes:
            return obj.classes.classes_name
        return obj.classes

    classes_classes_name.short_description = '班级名'


admin.site.register(TranslateClass, TranslateClassAdmin)
admin.site.site_header = u'网信安全考试系统管理'
admin.site.site_title = '网信安全考试系统管理'
admin.site.index_title = '数据管理'

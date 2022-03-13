from django.db.models.functions import Concat
from django.http import JsonResponse, QueryDict
from django.views import View
from django.core import serializers

from . import score_util
from .models import Subject, StudentSubject, TranslateClass, Translate, Classes
import json
from ExaminationManage import err_code
from ..users.models import UserProfile
from apps.users.login_utils import get_username, check_token


class Subjects(View):
    '''
        老师新增试题
        老师查询试题
    '''

    def get(self, request):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        subjects = Subject.objects.filter()

        province = serializers.serialize("json", subjects)
        result["data"] = json.loads(province)
        result["count"] = subjects.count()
        return JsonResponse(result)

    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        try:
            add_data = request.POST.get("addData")
            # score = request.POST.get("score")
            # subject_unswer = request.POST.get("subject_unswer")
        except:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "缺少参数"
            return JsonResponse(result)
        add_data_json = json.loads(add_data)

        subject = Subject()
        subject.subject_name = add_data_json["subject_name"]
        subject.subject_unswer = add_data_json["subject_unswer"]
        subject.score = add_data_json["score"]
        try:
            subject.save()
        except:
            result["msg"] = "添加失败"
            result["code"] = err_code.ADD_ERROR
            return JsonResponse(result)
        return JsonResponse(result)


# 修改
class PutSubjects(View):
    def post(self, request, pk):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        try:
            subjects = Subject.objects.get(id=pk)
        except Subject.DoesNotExist:
            result["code"] = err_code.PUT_ERROR
            return JsonResponse(result)

        column = request.POST.get("column", "")
        '1'.lower()
        tar_value = request.POST.get("tarValue", "")
        print(column)
        if column == "subject_name":
            subjects.subject_name = tar_value
        if column == "score":
            subjects.score = tar_value
        if column == "subject_class":
            subjects.subject_class = tar_value
        if column == "subject_unswer":
            subjects.subject_unswer = tar_value
        subjects.save()
        # Subject().update(column, tarValue, pk)
        return JsonResponse(result)


# 删除
class DelSubjects(View):
    def post(self, request, pk):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        subjects = None
        try:
            subjects = Subject.objects.get(id=pk)
        except Subject.DoesNotExist:
            result["code"] = err_code.DELETE_ERROR
            return JsonResponse(result)

        try:
            subjects.delete()
        except:
            result["msg"] = "删除失败"
            result["code"] = err_code.ADD_ERROR
            return JsonResponse(result)
        return JsonResponse(result)


'''
试卷
'''


class TranslateIdClassView(View):
    def get(self, request, pk):
        '''
        试卷id查班级
        :param request:
        :param pk:
        :return:
        '''
        result = {"code": err_code.SUCCESS, "msg": "", "data": []}
        # 试卷Id
        translate_class = TranslateClass.objects.filter(id=pk).all()
        for translate in translate_class:
            re = {}
            re["classes_name"] = translate.classes.classes_name
            result.append(re)
        return JsonResponse(result)


class TranslateView(View):
    def get(self, request, pk):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        # 试卷Id

        if pk == "":
            result["code"] = err_code.SELECT_ERROR
            result["msg"] = "缺少参数"
            return JsonResponse(result)

        # 试卷下对应的题目Id和题目
        subjects = Translate.objects.filter(translate_class_id=pk)
        if subjects.count() == 0:
            result["code"] = err_code.UPDATE_ERROR
            result["msg"] = "该试卷没有题目"
            return JsonResponse(result)
        subjects_name_list = []
        for i in subjects:
            subjects_json = {}
            subjects_json["translate_id"] = i.id
            subjects_json["subject_name"] = Subject.objects.get(id=i.subject_id).subject_name
            subjects_name_list.append(subjects_json)
        result["data"] = subjects_name_list
        return JsonResponse(result)

    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        try:
            subject_id = request.POST.get("subject_id", -1)
            translate_class_id = request.POST.get("translate_class_id")
        except BaseException:
            result["msg"] = "请先添加试卷"
            result["code"] = err_code.DELETE_ERROR
            return JsonResponse(result)
        if translate_class_id == -1:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "请先添加试卷"
            return JsonResponse(result)
        is_translate = Translate.objects.filter(subject_id=subject_id, translate_class_id=translate_class_id)
        if is_translate.count() > 0:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "试卷已经存在此题"
            return JsonResponse(result)
        print(subject_id, '==', translate_class_id)
        translate = Translate()
        translate.subject_id = subject_id
        translate.translate_class_id = translate_class_id
        try:
            translate.save()
        except translate.DoesNotExist:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "试卷不存在"
            return JsonResponse(result)
        return JsonResponse(result)


class DelTranslateView(View):
    def post(self, request, pk):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        translate = None
        try:
            translate = Translate.objects.get(id=pk)
        except Subject.DoesNotExist:
            result["code"] = err_code.DELETE_ERROR
            return JsonResponse(result)

        try:
            translate.delete()
        except:
            result["msg"] = "删除失败"
            result["code"] = err_code.ADD_ERROR
            return JsonResponse(result)
        return JsonResponse(result)


class PutTranslateView(View):
    def post(self, request):
        # translate_class_name
        # exam_class
        return JsonResponse


'''
    试卷
'''


class TranslateClassView(View):
    def get(self, request):
        result = {"code": err_code.SUCCESS, "msg111": "", "data": []}
        translate_class = TranslateClass.objects.all()
        for translate in translate_class:
            re = {}
            re["pk"] = translate.id
            re["class_name"] = translate.class_name
            re["start_time"] = translate.start_time
            re["end_time"] = translate.end_time
            re["classes_name"] = translate.classes.classes_name
            result["data"].append(re)

        result["count"] = translate_class.count()
        return JsonResponse(result)

    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "成功", "data": ""}
        # 增加试卷分类
        # 试卷类名
        try:
            add_data = request.POST.get("addData", "")
            add_data_json = json.loads(add_data)
            # score = request.POST.get("score")
            # subject_unswer = request.POST.get("subject_unswer")
        except:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "缺少参数"
            return JsonResponse(result)

        classes_id = add_data_json["classes_name"]
        exam_class = add_data_json["shijuanming"]

        translate_class_count = TranslateClass.objects.filter(class_name=exam_class).count()
        if translate_class_count > 0:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "该试卷已经存在"
            return JsonResponse(result)

        translate_class = TranslateClass()
        print(classes_id)
        print(exam_class)
        translate_class.classes_id = classes_id
        translate_class.class_name = exam_class
        try:
            translate_class.save()
        except BaseException:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "添加失败"
            return JsonResponse(result)
        return JsonResponse(result)


class DelTranslateClass(View):
    def post(self, request, pk):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        translate_class = None
        try:
            translate_class = TranslateClass.objects.get(id=pk)
        except Subject.DoesNotExist:
            result["code"] = err_code.DELETE_ERROR
            return JsonResponse(result)

        try:
            translate_class.delete()
        except:
            result["msg"] = "删除失败"
            result["code"] = err_code.ADD_ERROR
            return JsonResponse(result)
        return JsonResponse(result)


class PutTranslateClass(View):
    def post(self, request, pk):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        try:
            translate_class = TranslateClass.objects.get(id=pk)
        except Subject.DoesNotExist:
            result["code"] = err_code.PUT_ERROR
            return JsonResponse(result)

        column = request.POST.get("column", "")
        tar_value = request.POST.get("tarValue", "")

        if column == "class_name":
            translate_class.class_name = tar_value
        elif column == "exam_class":
            translate_class.exam_class = tar_value
        else:
            result["code"] = err_code.PUT_ERROR
            result["msg"] = "修改失败"
            return JsonResponse(result)

        translate_class.save()
        return JsonResponse(result)


class ClassesView(View):
    def get(self, request):
        result = {"code": err_code.SUCCESS, "查询成功": "", "data": ""}
        subjects = Classes.objects.all()
        province = serializers.serialize("json", subjects)
        result["data"] = json.loads(province)
        result["count"] = subjects.count()
        return JsonResponse(result)

    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "创建成功", "data": ""}
        try:
            classes_name = request.POST.get("class_name", "")
        except BaseException:
            result["msg"] = "缺少参数"
            result["code"] = err_code.ADD_ERROR
            return JsonResponse(result)
        if classes_name == "":
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "请输入班级"
            return JsonResponse(result)

        is_translate = Classes.objects.filter(classes_name=classes_name)
        if is_translate.count() > 0:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "该班级已经存在"
            return JsonResponse(result)
        classes = Classes()
        classes.classes_name = classes_name
        try:
            classes.save()
        except classes.DoesNotExist:
            result["code"] = err_code.ADD_ERROR
            result["msg"] = "已经创建"
            return JsonResponse(result)
        return JsonResponse(result)


class StudentSubjectView(View):
    def get(self, request, pk):
        '''
        根据试卷id,查看所有学生的答题卡
        :param request:
        :param pk:
        :return:
        '''
        result = {"code": err_code.SUCCESS, "msg111": "", "data": []}
        student_subjects = StudentSubject.objects.filter(translate_class=pk)
        for student_subject in student_subjects:
            re = {}
            re["pk"] = student_subject.id
            re["stu_number"] = student_subject.userprofile.stu_number
            re["the_name"] = student_subject.userprofile.the_name
            re["subject_answer"] = student_subject.subject.subject_unswer
            re["user_answer"] = student_subject.subject_answer
            re["auto_score"] = student_subject.auto_score
            re["user_score"] = student_subject.user_score
            re["is_auto_score"] = student_subject.is_auto_score
            re["subject_name"] = student_subject.subject.subject_name
            result["data"].append(re)

        result["count"] = student_subjects.count()
        return JsonResponse(result)


class StartSubjects(View):
    def post(self, request, pk):
        """
        根据试卷id,查看所有学生的题目
        :param request:
        :param pk:
        :return:
        """
        result = {"code": err_code.SUCCESS, "msg": "", "data": []}
        token = request.POST.get("token", "")
        if not check_token(token):
            result = {"code": err_code.START_LOGIN, "msg": "登录失效", "data": ""}
            return JsonResponse(result)

        user_name = get_username(token)
        user_profile = UserProfile.objects.get(user_name=user_name)

        # 试卷下的题目
        translates = Translate.objects.filter(translate_class=pk)
        # 将查到的题目添加到学生题目表里面
        for translate in translates:
            student_subjects = StudentSubject()
            # 如果题目已经存在，
            if StudentSubject.objects.filter(userprofile=user_profile.id, translate_class=translate.translate_class,
                                             subject_id=translate.subject_id, ).count() > 0:
                continue
            student_subjects.userprofile_id = user_profile.id
            student_subjects.translate_class_id = pk
            student_subjects.subject = translate.subject
            student_subjects.save()

        # 查询学生的题目返回
        print(user_profile.id, '==', pk)
        re_student_subjects = StudentSubject.objects.filter(userprofile_id=user_profile.id, translate_class=pk)
        for re_subject in re_student_subjects:
            re = {"pk": re_subject.id, "subject_name": re_subject.subject.subject_name}
            result["data"].append(re)

        result["count"] = re_student_subjects.count()
        return JsonResponse(result)


class PutSubjectsView(View):
    def post(self, request, pk):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        try:
            student_sub = StudentSubject.objects.get(id=pk)
        except Subject.DoesNotExist:
            result["code"] = err_code.PUT_ERROR
            return JsonResponse(result)

        column = request.POST.get("column", "")
        tar_value = request.POST.get("tarValue", "")

        if column == "auto_score":
            student_sub.auto_score = tar_value
        elif column == "user_score":
            student_sub.user_score = tar_value
        elif column == "is_auto_score":
            student_sub.is_auto_score = tar_value
        else:
            result["code"] = err_code.PUT_ERROR
            result["msg"] = "修改失败"
            return JsonResponse(result)
        student_sub.save()
        return JsonResponse(result)


class ListStuTranslateClass(View):
    def post(self, request):
        # 检查登录
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        token = request.POST.get("token", "")
        if not check_token(token):
            result = {"code": err_code.START_LOGIN, "msg": "没有登录", "data": ""}
            return JsonResponse(result)
        user_name = get_username(token)
        user_profile = UserProfile.objects.get(user_name=user_name)

        translate_class = TranslateClass.objects.filter(classes_id=user_profile.classes)

        re_data = []
        for translate in translate_class:
            re = {}
            re["pk"] = translate.id
            re["class_name"] = translate.class_name
            re["start_time"] = translate.start_time
            re["end_time"] = translate.end_time
            re_data.append(re)
        result["data"] = re_data
        return JsonResponse(result)


class PutBatchStudentSubject(View):
    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        answer_json = json.loads(request.POST.get("answerData"))
        print(answer_json)
        for key in answer_json:
            student_sub = StudentSubject.objects.get(id=key)
            student_sub.subject_answer = answer_json[key]
            student_sub.save()

        return JsonResponse(result)


class GetStuAnswerSubjectView(View):
    def post(self, request):
        '''
        根据试卷id,查看所有学生的答题卡
        :param request:
        :param pk:
        :return:
        '''
        # 检查登录
        result = {"code": err_code.SUCCESS, "msg": "", "data": []}
        token = request.POST.get("token", "")
        pk = request.POST.get("pk", "")
        if not check_token(token):
            result = {"code": err_code.START_LOGIN, "msg": "登录失效", "data": ""}
            return JsonResponse(result)

        user_name = get_username(token)
        user_profile = UserProfile.objects.get(user_name=user_name)

        student_subjects = StudentSubject.objects.filter(translate_class=pk, userprofile=user_profile.id)
        for student_subject in student_subjects:
            re = {}
            re["pk"] = student_subject.id
            re["user_subject_answer"] = student_subject.subject_answer

            re["auto_score"] = "暂无" if student_subject.auto_score == -1 else student_subject.auto_score
            re["user_score"] = "暂无" if student_subject.user_score == -1 else student_subject.user_score

            re["is_auto_score"] = student_subject.is_auto_score
            re["score"] = "暂无" if student_subject.subject.score == -1 else student_subject.subject.score
            re["subject_answer"] = student_subject.subject.subject_unswer
            re["subject_name"] = student_subject.subject.subject_name
            result["data"].append(re)

        result["count"] = student_subjects.count()
        return JsonResponse(result)


class AutoScoreSubject(View):
    def post(self, request):
        # 检查登录
        result = {"code": err_code.SUCCESS, "msg": "", "data": {}}
        token = request.POST.get("token", "")
        pk = request.POST.get("pk", "")
        if not check_token(token):
            result = {"code": err_code.START_LOGIN, "msg": "登录失效", "data": ""}
            return JsonResponse(result)
        stu_subject = StudentSubject.objects.get(id=pk)
        auto_score = score_util.auto_score(stu_subject.subject_answer, stu_subject.subject.subject_unswer)
        print(auto_score)
        result["data"]["score"] = auto_score

        stu_subject.auto_score = auto_score
        stu_subject.is_auto_score = 0
        stu_subject.save()
        return JsonResponse(result)

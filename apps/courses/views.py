import datetime
import json
import time
from functools import wraps

from django.http import (
    JsonResponse,
    QueryDict
)
from django.views import View
from django.core import serializers
from django.db.models import F, Sum

from ExaminationManage.settings import UPLOAD_PATH
from . import score_util
from .models import (
    Subject,
    StudentSubject,
    TranslateClass,
    Translate,
    Classes,
    StudentRecordingScreen,
    SINGLE_CHOICE,
    MULTIPLE_CHOICE,
    JUDGMENT,
    Judgment
)
from ExaminationManage import err_code
from ..users.models import UserProfile
from apps.users.login_utils import get_username, check_token

SPLIT_CHAR = "&"


def check_login(func):
    """
    登录认证装饰器
    params: func:是被装饰的方法
    # wraps的作用就是不会修改被装饰的方法名(防止多个装饰器重叠报错)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        *args和*kwargs不懂的可以自己网上查下
        """
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        token = args[0].request.META.get("HTTP_AUTHORIZATION", "")
        if not check_token(token):
            result['code'] = err_code.START_LOGIN
            result['msg'] = u'登录失效'
            return JsonResponse(result)
        user_name = get_username(token)
        user_profile = UserProfile.objects.get(user_name=user_name)
        kwargs['user_profile'] = user_profile
        return func(*args, **kwargs)

    return wrapper


class Subjects(View):
    """
        老师新增试题、查询试题
        0:单选题:
            题目埃里克森卡就发多少
            321
            答案：A
        1:多选题
            答案：[]
        2:判断题:
            答案：0：正确 1：错误
        3:填空题
        4:简答题
    """

    def __init__(self):
        self.subject_db = Subject()

    def get(self, request):
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        subjects = Subject.objects.filter()

        province = serializers.serialize("json", subjects)
        result["data"] = json.loads(province)
        result["count"] = subjects.count()
        return JsonResponse(result)

    def post(self, request):
        """
        :param request:
        :return:
        """
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        body = json.loads(str(request.body, 'utf-8'))
        subject_type = int(body.get('subject_type', -1))
        subject_name = body.get('subject_name', '')
        subject_answer = body.get('subject_unswer', '')
        score = body.get('score', '-1')
        subject_name = subject_name.split('\n')
        subject_answer = subject_answer.split('\n')

        for i, name in enumerate(subject_name):
            subject_name[i] = name.strip()
        for i, answer in enumerate(subject_answer):
            subject_answer[i] = answer.strip()
        print(f'subject_names:{subject_name}')
        print(f'subject_answer:{subject_answer} type: {type(subject_answer)}')

        if subject_type == SINGLE_CHOICE:
            # 处理单选题
            # ['题目', '选项一', '选项二']
            if len(subject_name) <= 1:
                result["code"] = err_code.ADD_ERROR
                result["msg"] = "单选题目格式错误"
                print(result["msg"])
                return JsonResponse(result)
            if subject_answer[0] not in subject_name[1:]:
                result["code"] = err_code.ADD_ERROR
                result["msg"] = "（单选题）用户答案不在题目选项中"
                print(result["msg"])
                return JsonResponse(result)
            subject_name = SPLIT_CHAR.join(subject_name)
        elif subject_type == MULTIPLE_CHOICE:
            # 处理多选题
            # ['题目', '选项一', '选项二']
            if len(subject_name) <= 1:
                result["code"] = err_code.ADD_ERROR
                result["msg"] = "多选题目格式错误"
                print(result["msg"])
                return JsonResponse(result)

            flag = True
            print(f'=====subject_names 79: {subject_name}')
            print(f'=====subject_answer 80: {subject_answer}')
            for answer in subject_answer:
                if answer not in subject_name[1:]:
                    flag = False
                    break
            if not flag:
                result["code"] = err_code.ADD_ERROR
                result["msg"] = "（多选题）用户答案不在题目选项中"
                print(result["msg"])
                return JsonResponse(result)
            subject_name = SPLIT_CHAR.join(subject_name)
        elif subject_type == JUDGMENT:
            print(f'=====subject_names 92: {subject_name}')
            print(f'=====subject_answer 93: {subject_answer}')
            if isinstance(subject_name, list) and len(subject_name) >= 2:
                result["code"] = err_code.ADD_ERROR
                result["msg"] = "判断题目不能换行"
                print(result["msg"])
                return JsonResponse(result)
            subject_answer = int(subject_answer[0])
            if subject_answer not in [Judgment.CORRECT, Judgment.ERROR]:
                result["code"] = err_code.ADD_ERROR
                result["msg"] = "判断题答案只能是0或1（1:错误，0正确）"
                print(result["msg"])
                return JsonResponse(result)
            subject_name, *_ = subject_name
        else:
            result["msg"] = "暂时不支持该题目类型"
            result["code"] = err_code.ADD_ERROR
            return JsonResponse(result)
        print(f'110 subject_name: {subject_name}')
        self.subject_db.subject_name = subject_name
        self.subject_db.subject_unswer = SPLIT_CHAR.join(subject_answer) if isinstance(
            subject_answer, list) else subject_answer
        self.subject_db.score = score
        self.subject_db.type = int(subject_type)
        try:
            self.subject_db.save()
        except Exception as e:
            result["msg"] = u'添加失败'
            result["code"] = err_code.ADD_ERROR
            print(e)
            return JsonResponse(result)
        result['msg'] = u'添加成功'

        return JsonResponse(result)

    # def handle_subject(self, subject_name, sub_type):
    #     """
    #     处理题目
    #     :param subject_name: str "<p>发的课件撒结果大家法律的凯撒奖霏霏械</p><p>A.123</p>"
    #     :param sub_type:
    #     :return:
    #     """
    #     subject_name.
    #     if sub_type == 0:


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
        except Exception:
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
        """
        根据试卷id,查看所有学生的答题卡
        :param request:
        :param pk:
        :return:{
            code: 0
            count: 1
            data: [{
                stu_number: "Z202014060634",
                the_name: "朱朱朱",
                sum_score: 20,
                // 回话地址
                recording_url: "16505393374499630.mp4"
            }]
            msg: ""
        }
        """
        result = {"code": err_code.SUCCESS, "msg": "", "data": []}
        student_subjects = StudentSubject.objects.filter(translate_class=pk).values('userprofile').annotate(
            sum_score=Sum('auto_score'), the_name=F('userprofile__the_name'), stu_number=F('userprofile__stu_number')
        )
        record = StudentRecordingScreen.objects.filter(translate_class=pk).first()
        for student_subject in student_subjects:
            result["data"].append({
                "stu_number": student_subject['stu_number'],
                "the_name": student_subject['the_name'],
                "sum_score": student_subject['sum_score'],
                "recording_url": record.file_name if record else ""
            })

        result["count"] = student_subjects.count()
        return JsonResponse(result)


class StartSubjects(View):
    @check_login
    def post(self, request, user_profile):
        result = {"code": err_code.SUCCESS, "msg": "视频上传成功", "data": []}
        files = request.FILES.get('file', '')
        test_paper_id = request.POST.get('testPaperId')
        print('test_paper_id:{}'.format(test_paper_id))
        *_, file_extension = files.name.split('.')
        random_file_name = ".".join([str(int(time.time() * 10000000)), file_extension])
        print(random_file_name)
        with open('{}/{}'.format(UPLOAD_PATH, random_file_name), "wb") as fs:
            for item in files.chunks():
                fs.write(item)
        student_record_db = StudentRecordingScreen()
        student_record_db.file_name = random_file_name
        student_record_db.userprofile_id = user_profile.id
        student_record_db.translate_class_id = test_paper_id
        student_record_db.save()
        return JsonResponse(result)

    @check_login
    def put(self, request, user_profile):
        """
        @api {put} /courses/commit_test_paper 提交试卷和评分
        @apiName CommitTestPaper
        @apiGroup Courses

        @apiBody {String} userName=admin 用户名
        @apiBody {String} passwd=admin 密码

        @apiSuccessExample {json} Success-Response:
        {
            "code": "登录成功",
            "msg": "",
            "data": {}
        }
        @apiErrorExample {json} Error-Response:
        {
            "code": 0,
            "msg": "",
            "data": {}
        }
        @apiSampleRequest /courses/commit_test_paper
        """
        result = {"code": err_code.SUCCESS, "msg": "交卷成功", "data": []}

        query_dict = QueryDict(request.body)
        sorted_topics = json.loads(query_dict.get('sortedTopics'))
        for topic in sorted_topics:
            if not topic:
                continue
            for content in topic['topic_content']:
                pk = content['pk']
                user_answer = SPLIT_CHAR.join(content['userAnswer'])
                print(f"user_answer:{user_answer}")
                student_subject = StudentSubject.objects.filter(id=pk).first()
                student_subject.subject_answer = user_answer
                if user_answer == student_subject.subject.subject_unswer:
                    # 用户答案和题目答案是否相等
                    student_subject.auto_score = student_subject.subject.score
                student_subject.save()
        return JsonResponse(result)

    @check_login
    def get(self, request, pk, user_profile):
        """
        url: /courses/stu_start_test/1
        根据试卷id,查看所有学生的题目
        :param request:
        :param pk:
        :param user_profile:
        :return:
        //题目类型==>  0:单选题  1:多选题  2:判断题  3:填空题  4:简答题
        sortedTopics: [
            {
                topicType: 0,
                topic_content: [{
                    index: 1
                    pk: 10
                    question: "多选1"
                    score: "10"
                    "choice": ["111223", "4213", "3214"],
                    topicType: 1 //题目类型
                    userAnswer: [] // 用户答案
                }]
            },
            {
                topicType: 1,
                topic_content: [{
                    "index": 1,
                    "question": "多选1",
                    "score": 24,
                    "choice": ["111223", "4213", "3214"],
                    "topicType": 1,
                    "userAnswer": []
                }]
            },
            {
                topicType: 2, topic_content: [{
                    "index": 1,
                    "question": "多选1",
                    "score": 24,
                    "choice": ["111223", "4213", "3214"],
                    "topicType": 2,
                    "userAnswer": "" // 0：正确 1：错误
                }]
            },
            {topicType: 3, topic_content: []},
            {topicType: 4, topic_content: []},
        ]
        """
        result = {"code": err_code.SUCCESS, "msg": "题目获取完成", "data": []}
        user_id = user_profile.id
        # 是否在考试时间内
        translate_class = TranslateClass.objects.filter(id=pk).first()
        now_time = datetime.datetime.now()
        if now_time < translate_class.start_time or now_time > translate_class.end_time:
            result['code'] = err_code.ADD_ERROR
            result['msg'] = u'不在考试时间范围内'
            return JsonResponse(result)

        # 试卷下的题目
        translates = Translate.objects.filter(translate_class=pk)
        # 将查到的题目添加到学生题目表里面
        for translate in translates:
            # 如果题目已经存在
            if StudentSubject.objects.filter(
                    userprofile=user_id,
                    translate_class=translate.translate_class,
                    subject_id=translate.subject_id
            ).count() > 0:
                continue
            student_subjects = StudentSubject()
            student_subjects.userprofile_id = user_id
            student_subjects.translate_class_id = pk
            student_subjects.subject = translate.subject
            student_subjects.save()

        # 查询学生的题目返回
        re_student_subjects = StudentSubject.objects.filter(userprofile_id=user_id, translate_class=pk).values(
            'id', 'subject_answer', score=F('subject__score'),
            subject_name=F('subject__subject_name'),
            subject_type=F('subject__type'),
            test_paper_name=F('translate_class__class_name')
        )

        # 单选题
        single_choice = []
        # 多选题
        multiple_choice = []
        # 判断题
        judgment = []
        # 试卷名
        test_paper_name = ''
        for re_subject in re_student_subjects:
            question, *choices = re_subject['subject_name'].split('&')
            test_paper_name = re_subject['test_paper_name']
            if re_subject['subject_type'] == 0:
                # 单选题
                single_choice.append({
                    "pk": re_subject['id'],
                    "index": single_choice[-1]['index'] + 1 if single_choice else 1,
                    "question": question,
                    "score": re_subject['score'],
                    "choice": choices,
                    "topicType": 0,
                    "userAnswer": [re_subject['subject_answer']] if re_subject['subject_answer'] else []
                })
            elif re_subject['subject_type'] == 1:
                # 多选题
                multiple_choice.append({
                    "pk": re_subject['id'],
                    "index": multiple_choice[-1]['index'] + 1 if multiple_choice else 1,
                    "question": question,
                    "score": re_subject['score'],
                    "choice": choices,
                    "topicType": 1,
                    "userAnswer": re_subject['subject_answer'].split(SPLIT_CHAR) if re_subject['subject_answer'] else []
                })
            elif re_subject['subject_type'] == 2:
                # 判断题
                print(f"re_subject['subject_answer']:{re_subject['subject_answer']}")
                print(f"question:{question}")
                judgment.append({
                    "pk": re_subject['id'],
                    "index": judgment[-1]['index'] + 1 if judgment else 1,
                    "question": question,
                    "score": re_subject['score'],
                    "topicType": 2,
                    "userAnswer": re_subject['subject_answer']
                })
            else:
                print(f"未知题目：pk{re_subject['id']}")
        result["data"] = {
            "testPaperName": test_paper_name,
            "allSubject": [
                {"topicType": 0, "topic_content": single_choice},
                {"topicType": 1, "topic_content": multiple_choice},
                {"topicType": 2, "topic_content": judgment}
            ],
            "endTime": translate_class.end_time.strftime('%Y-%m-%d %H:%M:%S')
        }
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
    @check_login
    def post(self, request, user_profile):
        # 检查登录
        result = {"code": err_code.SUCCESS, "msg": "", "data": ""}
        translate_class = TranslateClass.objects.filter(classes_id=user_profile.classes)

        re_data = []
        for translate in translate_class:
            re = {
                "pk": translate.id,
                "class_name": translate.class_name,
                "start_time": translate.start_time,
                "end_time": translate.end_time
            }
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
    @check_login
    def post(self, request, user_profile):
        """
        根据试卷id,查看所有学生的答题卡
        :param request:
        :param pk:
        :return:
        """
        # 检查登录
        result = {"code": err_code.SUCCESS, "msg": "加载成功", "data": []}
        pk = request.POST.get("pk", "")

        student_subjects = StudentSubject.objects.filter(translate_class=pk, userprofile=user_profile.id)
        sum_score = 0
        for student_subject in student_subjects:
            if student_subject.auto_score > 0:
                sum_score += student_subject.auto_score

            subject_answer = student_subject.subject_answer
            subject_type = student_subject.subject.type
            if subject_type == JUDGMENT:
                subject_answer = "正确" if int(subject_answer) == Judgment.CORRECT else "错误"
            re = {
                "pk": student_subject.id,
                "user_subject_answer": subject_answer,
                "auto_score": 0 if student_subject.auto_score == -1 else student_subject.auto_score,
                "user_score": 0 if student_subject.user_score == -1 else student_subject.user_score,
                "is_auto_score": student_subject.is_auto_score,
                "score": 0 if student_subject.subject.score == -1 else student_subject.subject.score,
                "subject_answer": student_subject.subject.subject_unswer,
                "subject_name": student_subject.subject.subject_name,
                "subject_type": Subject.get_subject_type(subject_type)
            }
            result["data"].append(re)

        result["count"] = student_subjects.count()
        result["sum_score"] = sum_score
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

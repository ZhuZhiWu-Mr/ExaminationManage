import json
import logging
from django.views import View
from django.http import JsonResponse
from . import login_utils
from .login_utils import check_token, get_username
from .models import UserProfile, Classes

from ExaminationManage import err_code


class SingIn(View):
    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "登录成功", "data": ""}
        user_name = request.POST.get("user_name")
        passwd = request.POST.get("passwd")
        # 判断用户名和账号
        user_info = UserProfile.objects.filter(user_name=user_name, passwd=passwd).first()
        if not user_info:
            result["msg"] = "账号或密码错误"
            result["code"] = err_code.SELECT_ERROR
            return JsonResponse(result)
        token = ""
        try:
            token = login_utils.create_token(user_name)
        except Exception as ce:
            logging.exception(f"我的异常：{ce}")
            result["msg"] = "服务器异常"
            result["code"] = err_code.SELECT_ERROR
            return JsonResponse(result)
        result_tmp = {
            "token": token,
            "nick_name": user_info.nick_name,
            "user_type": user_info.user_type
        }
        result["data"] = result_tmp
        return JsonResponse(result)


class SingOut(View):
    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "已经登录", "data": {}}
        token = request.POST.get("token")
        result["data"]["is_login"] = login_utils.check_token(token)
        return JsonResponse(result)


class SingUp(View):
    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "注册成功", "data": {}}
        user_name = request.POST.get("user_name")
        passwd = request.POST.get("passwd")
        classes = request.POST.get("clsses")
        user_type = request.POST.get("user_type", 2)
        # 老师
        if user_type == 2:
            classes = request.POST.get("classes")
        print(user_name)
        user_name_count = UserProfile.objects.filter(user_name=user_name).count()
        print(user_name_count)
        if user_name_count > 0:
            result["msg"] = "账号已经存在"
            result["code"] = err_code.ADD_ERROR
            return JsonResponse(result)
        user_profile = UserProfile()
        user_profile.user_name = user_name
        user_profile.passwd = passwd
        user_profile.user_type = user_type
        user_profile.classes_id = classes
        user_profile.save()
        return JsonResponse(result)


class ListUserProfile(View):
    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "", "data": {}}
        token = request.POST.get("token")
        if not check_token(token):
            result = {"code": err_code.START_LOGIN, "msg": "登录失效", "data": ""}
            return JsonResponse(result)
        user_name = get_username(token)

        user_profile = UserProfile.objects.get(user_name=user_name)
        result["data"]["the_name"] = user_profile.the_name
        result["data"]["stu_number"] = user_profile.stu_number
        result["data"]["nick_name"] = user_profile.nick_name
        result["data"]["classes_name"] = user_profile.classes.classes_name if user_profile.classes else ""
        result["data"]["classes_id"] = user_profile.classes.id if user_profile.classes else ""
        result["data"]["passwd"] = user_profile.passwd
        result["data"]["classes"] = list(Classes.objects.filter().values())
        return JsonResponse(result)


class PutUserProfile(View):
    def post(self, request):
        result = {"code": err_code.SUCCESS, "msg": "", "data": {}}
        token = request.POST.get("token")
        if not check_token(token):
            result = {"code": err_code.START_LOGIN, "msg": "登录失效", "data": ""}
            return JsonResponse(result)
        user_name = get_username(token)
        json_data = json.loads(request.POST.get("data"))

        the_name = json_data["the_name"]
        stu_number = json_data["stu_number"]
        nick_name = json_data["nick_name"]
        passwd = json_data["passwd"]
        classes = json_data["classes"]

        user_profile = UserProfile.objects.get(user_name=user_name)
        user_profile.user_name = user_name
        user_profile.the_name = the_name
        user_profile.stu_number = stu_number
        user_profile.nick_name = nick_name
        user_profile.passwd = passwd
        user_profile.classes_id = classes
        user_profile.save()
        return JsonResponse(result)

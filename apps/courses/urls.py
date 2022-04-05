from django.conf.urls import url

from . import views

urlpatterns = {
    # url(r'^subjects/(?P<pk>\d+)/$', views.Subjects),
    url(r'^subjects$', views.Subjects.as_view()),
    url(r'^del_subjects/(?P<pk>\d+)$', views.DelSubjects.as_view()),
    url(r'^put_subjects/(?P<pk>\d+)$', views.PutSubjects.as_view()),

    # 添加试卷、查询试卷类别
    url(r'^list_translate_class$', views.TranslateClassView.as_view()),

    # 删除试卷类别
    url(r'^del_translate_class/(?P<pk>\d+)$', views.DelTranslateClass.as_view()),

    # 修改试卷类别
    url(r'^put_translate_class/(?P<pk>\d+)$', views.PutTranslateClass.as_view()),

    # 为试卷添加题目，post
    url(r'^add_translate$', views.TranslateView.as_view()),

    # 根据试卷id查看班级
    url(r'^translate_id_class/(?P<pk>\d+)$', views.TranslateIdClassView.as_view()),

    # 根据试卷id查询试卷题目id
    url(r'^list_translate/(?P<pk>\d+)$', views.TranslateView.as_view()),

    # 删除试卷题目
    url(r'^del_translate/(?P<pk>\d+)$', views.DelTranslateView.as_view()),
    # 修改试卷题目

    # 根据试卷查看所对应的学生+答题卡
    url("^student_subject/(?P<pk>\d+)$", views.StudentSubjectView.as_view()),

    # 自动评分、人工分数修改
    url("^put_student_score/(?P<pk>\d+)$", views.PutSubjectsView.as_view()),

    # 获取班级
    url("^classes$", views.ClassesView.as_view()),

    # 查看学生对应的考试
    url("^list_stu_translate_class$", views.ListStuTranslateClass.as_view()),

    # 开始考试，获取试卷的题目
    url("^stu_start_test/(?P<pk>\d+)$", views.StartSubjects.as_view()),

    # 提交试卷 【PUT】
    url("^commit_test_paper", views.StartSubjects.as_view()),

    # 批量修改学生答案
    url("^put_batch_student_subject$", views.PutBatchStudentSubject.as_view()),

    # 使用试卷id，查看单个学生对应的答题卡
    url("^list_stu_answer_subject$", views.GetStuAnswerSubjectView.as_view()),

    # 自动评分接口
    url("^auto_score_subject$", views.AutoScoreSubject.as_view())
}

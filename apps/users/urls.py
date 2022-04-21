from django.conf.urls import include, url

from . import views

urlpatterns = [
    # url(r'^subjects/(?P<pk>\d+)/$', views.Subjects),
    url(r'^singin$', views.SingIn.as_view()),
    url(r'^sing_out$', views.SingOut.as_view()),
    url(r'^singup$', views.SingUp.as_view()),
    url(r'^list_user_profile$', views.ListUserProfile.as_view()),
    url(r'^put_user_profile$', views.PutUserProfile.as_view())
]
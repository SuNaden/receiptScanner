from django.conf.urls import url
from main import views
from main.forms import LoginForm

urlpatterns = [
    url(r'^home/$', views.Home.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'main/signin.html', 'authentication_form': LoginForm}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^budget/$', views.BudgetView.as_view()),
    url(r'^budget/budget$', views.BudgetView.as_view()),
    url(r'^statistics/$', views.StatisticsView.as_view()),
    url(r'^budget/statistics/$', views.StatisticsView.as_view()),
    url(r'^budget/statistics/budget$', views.BudgetView.as_view()),
    url(r'^history/$', views.Home.as_view()),
    url(r'^budget/history$', views.Home.as_view()),
    url(r'^statistics/history$', views.Home.as_view()),

]

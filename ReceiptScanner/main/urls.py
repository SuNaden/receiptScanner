from django.conf.urls import url
from main import views
from main.forms import LoginForm

urlpatterns = [
    url(r'^home/$', views.ReceiptsHistory.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'main/signin.html', 'authentication_form': LoginForm}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^budget/$', views.BudgetView.as_view()),
    url(r'^statistics/$', views.StatisticsView.as_view()),
    url(r'^history/$', views.ReceiptsHistory.as_view()),
    url(r'^delete/receipt/(?P<id>[0-9]+)$', views.DeleteReceipt.as_view()),

]

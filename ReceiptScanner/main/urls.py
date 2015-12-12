from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^home/$', views.Home.as_view()),
]

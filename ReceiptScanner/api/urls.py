from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^upload/$', views.Upload.as_view()),
    url(r'^login/$', views.Login.as_view())
]

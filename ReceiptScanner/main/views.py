from django.shortcuts import render
from django.views.generic.base import TemplateView

class Home(TemplateView):
  template_name = "main/index.html"

  def dispatch(self, *args, **kwargs):
    return super(HomeView, self).dispatch(*args, **kwargs)
from django.shortcuts import render
from django.views.generic.base import TemplateView

class Home(TemplateView):
  template_name = "main/index.html"

  def get(self, request):
    return render(request, self.template_name, None)
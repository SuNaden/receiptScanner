from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
import api.models 




class Home(TemplateView):
  template_name = "main/home.html"
  
  @method_decorator(login_required)
  def get(self, request):
    return render(request, self.template_name)


class RegisterView(TemplateView):
  template_name = "main/register.html"
  page_title = "Register"
  form = None

  def get_context_data(self, **kwargs):
    context = super(RegisterView, self).get_context_data(**kwargs)
    context["page_title"] = self.page_title
    context["form"] = self.form
    return context

  def post(self, request):
    self.form = RegisterForm(request.POST)
    if self.form.is_valid():
      email = self.form.cleaned_data['email']
      username = self.form.cleaned_data['username']
      password = self.form.cleaned_data['password1']
      user = User.objects.create_user(username, email, password)

      return render(request, "main/home.html", self.get_context_data())
    else:
      return render(request, self.template_name, self.get_context_data())

  def get(self, request):
    self.form = RegisterForm()
    return render(request, self.template_name, self.get_context_data())

class BudgetView(TemplateView):
  
  @method_decorator(login_required)
  def get(self, request):
    #Get list of receipts
    currentUser = request.user
    today = datetime.date.today()
    currentMonth = today.month
    currentYear = today.year
    receipts = 0


    Receipts.objects.filter(user = currentUser, date__year = currentYear, date__month = currentMonth)

    #Get budget spent and number of items
    spentBudget = 0
    itemsNumber = 0
    
    for receipt in receipts:
      items = receipt.receiptItem_set.all()
      itemsNumber += items.count()
      for item in items:
        spentBudget += item.price

    #Get current monthly budget
    currentBudget = BudgetPeriod.objects.filter(start_date__month = currentMonth)[0]
    spendingLimit = currentBudget.spending_limit

    #Get left budget
    leftBudget = spendingLimit - spentBudget


    return render(request, "main/budget.html")



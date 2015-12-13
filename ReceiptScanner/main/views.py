from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime
from api.models import Receipt, Store
from api.models import BudgetPeriod

class DeleteReceipt(RedirectView):
  def get_redirect_url(self, *args, **kwargs):
    receipt = get_object_or_404(Receipt, pk=kwargs['id'])
    receipt.delete()
    return "/main/home"

class ReceiptsHistory(TemplateView):

  def get_context_data(self, **kwargs):
    context = super(ReceiptsHistory, self).get_context_data(**kwargs)

    #Get list of receipts
    currentUser = self.request.user
    receipts = Receipt.objects.filter(user = currentUser)

    context["receipts"] = receipts
    return context
  
  @method_decorator(login_required)
  def get(self, request):
    return render(request, "main/home.html", self.get_context_data())

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

  def get_context_data(self, **kwargs):
    context = super(BudgetView, self).get_context_data(**kwargs)

    #Get list of receipts
    currentUser = self.request.user
    today = datetime.date.today()
    currentMonth = today.month
    currentYear = today.year
    receipts = Receipt.objects.filter(user = currentUser, date__year = currentYear, date__month = currentMonth)
    receiptsNumber = receipts.count()

    #Get budget spent and number of items
    spentBudget = 0
    itemsList = []

    
    for receipt in receipts:
      items = receipt.receiptitem_set.all()
      for item in items:
        spentBudget += item.price
        itemsList.append(item)

    #Get current monthly budget
    print("Current: " + str(currentMonth))
    budget = BudgetPeriod.objects.get(user = currentUser, start_date__month = currentMonth)
    print(str(budget.spending_limit))

    #Get left budget
    leftBudget = budget.spending_limit - spentBudget
    percentage = (leftBudget / budget.spending_limit) * 100
    
    context["receipts"] = receipts
    context["spentBudget"] = spentBudget
    context["spendingLimit"] = budget.spending_limit
    context["leftBudget"] = leftBudget
    context["items"] = itemsList
    context["percentage"] = percentage
    return context
  
  @method_decorator(login_required)
  def get(self, request):
    return render(request, "main/budget.html", self.get_context_data())

class StatisticsView(TemplateView):

  def get_context_data(self, **kwargs):
    context = super(StatisticsView, self).get_context_data(**kwargs)
    
    currentUser = self.request.user
    receipts = Receipt.objects.all().filter(user = currentUser)
    totalSpending = 0
    totalItemsBought = 0

    for receipt in receipts:
      items = receipt.receiptitem_set.all()
      for item in items: 
        totalItemsBought += 1
        totalSpending += item.price

    numberOfMonths = BudgetPeriod.objects.all().count()
    averageSpending = totalSpending / numberOfMonths
    averageItemsBought = totalItemsBought / numberOfMonths

    stores = Store.objects.all()
    mostFrequentStore = None
    frequency = 0

    for store in stores:
      currentFrequency = store.receipt_set.all().count()
      if frequency < currentFrequency:
        frequency = currentFrequency
        mostFrequentStore = store

    context["totalSpending"] = totalSpending
    context["totalItemsBought"] = totalItemsBought
    context["averageSpending"] = averageSpending
    context["averageItemsBought"] = averageItemsBought
    context["mostFrequentStore"] = mostFrequentStore

    return context


  @method_decorator(login_required)
  def get(self, request):
    return render(request, "main/statistics.html", self.get_context_data())








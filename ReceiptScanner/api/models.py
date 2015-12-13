from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
  name = models.CharField(max_length=255)
  location = models.CharField(max_length=255)

class Receipt(models.Model):
  user = models.ForeignKey(User)
  names_image = models.ImageField(upload_to='names/')
  prices_image = models.ImageField(upload_to='prices/')
  date = models.DateTimeField(auto_now_add=True)
  description = models.CharField(max_length=255)
  store = models.ForeignKey(Store, null=True, blank=True)

class Category(models.Model):
  name = models.CharField(max_length=255)

class ReceiptItem(models.Model):
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=20, decimal_places=10)
  category = models.ManyToManyField(Category)
  receipt = models.ForeignKey(Receipt)

class BudgetPeriod(models.Model):
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  spending_limit = models.DecimalField(max_digits=20, decimal_places=10)
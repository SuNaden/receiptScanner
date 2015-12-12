from django.db import models

class Receipt(models.Model):
  names_image = models.ImageField(upload_to='receipts/')
  prices_image = models.ImageField(upload_to='prices/')
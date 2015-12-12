from django.db import models

class Receipt(models.Model):
  image = models.ImageField(upload_to='receipts/')
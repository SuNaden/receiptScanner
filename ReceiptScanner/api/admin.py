from django.contrib import admin

from api.models import Store, Receipt, Category, ReceiptItem, BudgetPeriod

# Register your models here.
admin.site.register(Store)
admin.site.register(Receipt)
admin.site.register(Category)
admin.site.register(ReceiptItem)
admin.site.register(BudgetPeriod)

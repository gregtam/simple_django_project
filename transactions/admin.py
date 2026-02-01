from django.contrib import admin
from .models import TransactionsModel, PlaidTransactionsModel

# Register your models here.
admin.site.register(TransactionsModel)
admin.site.register(PlaidTransactionsModel)
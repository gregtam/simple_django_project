from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('plaid_transactions_partial', views.plaid_transactions_partial, name='plaid_transactions_partial'),
]

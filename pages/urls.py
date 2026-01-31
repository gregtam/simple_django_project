from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('data', views.data, name='data'),
    path('contact', views.contact, name='contact'),
    path('slow_load_test_transactions', views.slow_load_test_transactions, name='slow_load_test_transactions'),
    path('transactions_table', views.transactions_table, name='transactions_table'),
    path('load_plaid_transactions', views.load_plaid_test_transactions, name='load_plaid_transactions'),
    path('plaid_transactions_table', views.plaid_transactions_table, name='plaid_transactions_table'),
]
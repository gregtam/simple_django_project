from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('data', views.data, name='data'),
    path('contact', views.contact, name='contact'),
    path('slow_load_test_transactions', views.slow_load_test_transactions, name='slow_load_test_transactions'),
    path('show_plaid_test_transactions', views.show_plaid_test_transactions, name='show_plaid_test_transactions'),
]
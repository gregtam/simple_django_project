from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('data', views.data, name='data'),
    path('contact', views.contact, name='contact'),
    path('celery_task', views.celery_task, name='celery_task'),
    path('transactions_table', views.transactions_table, name='transactions_table'),
]
from datetime import datetime
import time

from django.shortcuts import render
from transactions.models import TransactionsModel
from .tasks import simple_sleep_task

# Create your views here.
def home(request):
    return render(request, 'pages/home.html', {})

def data(request):
    transactions = TransactionsModel.objects.filter(user_uuid=request.user.uuid)

    return render(request, 'pages/data.html', {'transactions': transactions})

def about(request):
    return render(request, 'pages/about.html', {})

def contact(request):
    return render(request, 'pages/contact.html', {})

def slow_load_test_transactions(request):
    return render(request, 'pages/slow_load_test_transactions.html')

def transactions_table(request):
    """Partial view that renders the transactions table"""
    task = simple_sleep_task.delay()
    task.get(timeout=600)  # Wait for the task to complete
    transactions = TransactionsModel.objects.filter(user_uuid=request.user.uuid)

    return render(request, 'pages/partials/transactions_table.html', {'transactions': transactions})
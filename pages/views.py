from datetime import datetime
import time

from django.shortcuts import render
from transactions.models import TransactionsModel, PlaidTransactionsModel
from .tasks import simple_sleep_task

# Create your views here.
def home(request):
    return render(request, 'pages/home.html', {})

def data(request):
    transactions = TransactionsModel.objects.filter(user_uuid=request.user.uuid)

    return render(request, 'pages/data.html', {'transactions': transactions})

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

def slow_load_test_transactions(request):
    return render(request, 'pages/slow_load_test_transactions.html')

def show_plaid_test_transactions(request):
    from django.core.paginator import Paginator

    all_transactions = PlaidTransactionsModel.objects.filter(user_uuid=request.user.uuid).order_by('-date')
    paginator = Paginator(all_transactions, 15)  # 15 transactions per page
    page_number = request.GET.get('page', 1)
    transactions = paginator.get_page(page_number)

    return render(request, 'pages/show_plaid_test_transactions.html', {'transactions': transactions})

def transactions_table(request):
    """Partial view that renders the transactions table"""
    task = simple_sleep_task.delay()
    task.get(timeout=600)  # Wait for the task to complete
    transactions = TransactionsModel.objects.filter(user_uuid=request.user.uuid)

    return render(request, 'pages/partials/transactions_table.html', {'transactions': transactions})
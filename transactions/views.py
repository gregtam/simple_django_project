from django.core.paginator import Paginator
from django.shortcuts import render
from .models import PlaidTransactionsModel


# Create your views here.
def transactions_table(request):
    """Partial view that renders the transactions table"""
    task = simple_sleep_task.delay()
    task.get(timeout=600)  # Wait for the task to complete
    transactions = TransactionsModel.objects.filter(user_uuid=request.user.uuid)

    return render(request, 'pages/partials/transactions_table.html', {'transactions': transactions})

def plaid_transactions_partial(request):
    """Partial view that returns paginated Plaid transactions for HTMX requests"""
    all_transactions = PlaidTransactionsModel.objects.filter(user_uuid=request.user.uuid).order_by('-date')
    paginator = Paginator(all_transactions, 15)  # 15 transactions per page

    # Gets the page number from the request GET parameters
    page_number = request.GET.get('page', 1)

    # Gets the transactions for the requested page
    transactions = paginator.get_page(page_number)

    return render(request, 'transactions/partials/plaid_transactions_partial.html', {'transactions': transactions})

from django.shortcuts import render
from transactions.models import TransactionsModel

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
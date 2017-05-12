from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import Account

# Create your views here.

from django.http import HttpResponse

def login(request):
    return HttpResponse("THIS IS THE LOGIN PAGE!")

def createAccount(request):
    return HttpResponse("Admin is creating an account.")

def userPortal(request, username, password):
    authentication = get_object_or_404()
    return HttpResponse("User Portal.")

def adminPortal(request):
    Accounts_list = Account.objects.order_by('-accountnum')
    template = loader.get_template('banking_app/index.html')
    context = { 'Accounts_list': Accounts_list,}
    return render(request, 'banking_app/index.html', context)

def manageCustomers(request):
    return HttpResponse("Managing Customers.")

def manageAccounts(request):
    return HttpResponse("Managing Accounts.")

def manageAccountTypes(request):
    return HttpResponse("Managing Account Types.")

def manageCustomers(request):
    return HttpResponse("Managing Customers.")

def accountSummary(request):
    return HttpResponse("User account summary.")

def withdraw(request):
    return HttpResponse("Withdraw money.")

def deposit(request):
    return HttpResponse("deposit money.")

def transfer(request):
    return HttpResponse("Transfer money.")

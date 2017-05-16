from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import *

# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

def login_page(request):
    return render(request, template_name='banking_app/login_page.html')

def login(request):
    user_name = request.POST['username']
    password = request.POST['password']
    user = Users.objects.raw("SELECT * from users where username = %s AND password = %s", [user_name, password])
    user = list(user)
    # user = list(Users.objects.raw("SELECT * from users"))
    if not user:
        return render(request, template_name= 'banking_app/login_page.html', context= {
            'error_message': "wrong username or password",
        })
    elif user.type:
        return HttpResponseRedirect(reverse('banking_app:adminPortal', args=(user.customerid)))
    else:
        return HttpResponseRedirect(reverse('banking_app:userPortal', args=(user.customerid)))

def createUser(request):
    return HttpResponse("create new user")

def createAccount(request):
    return HttpResponse("Admin is creating an account.")

def userPortal(request, username, password):
    return HttpResponse("User Portal.")

def adminPortal(request):
    template = loader.get_template('banking_app/adminPortal.html')
    return render(request, 'banking_app/adminPortal.html')

def manageAccounts(request):
    return HttpResponse("Managing Accounts.")

def manageAccountTypes(request):
    AccountTypes = Accounttype.objects.raw("SELECT * from accounttype")
    context = {'AccountTypes' : AccountTypes,}
    return render(request, 'banking_app/manage_account_type.html', context)

def manageCustomers(request):
    customers = Customer.objects.raw("SELECT * from customer")
    print(customers)
    return HttpResponse("Managing Customers.")

def accountSummary(request):
    return HttpResponse("User account summary.")

def withdraw(request):
    return HttpResponse("Withdraw money.")

def deposit(request):
    return HttpResponse("deposit money.")

def transfer(request):
    return HttpResponse("Transfer money.")

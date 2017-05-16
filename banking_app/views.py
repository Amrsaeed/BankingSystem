from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.db import connection
from .models import *
from django.db import connection
# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

def login(request):
    if not request.POST:
        return render(request, template_name='banking_app/login_page.html')
    user_name = request.POST['username']
    password = request.POST['password']
    user = Users.objects.raw("SELECT * from users where username = %s AND password = %s", [user_name, password])
    user = list(user)
    # user = list(Users.objects.raw("SELECT * from users"))
    # print(user[0].id)
    if not user:
        return render(request, template_name='banking_app/login_page.html', context={
            'error_message': "wrong username or password",
        })
    elif user[0].type:
        request.session['user_id'] = user[0].id
        return HttpResponseRedirect(reverse('banking_system:adminPortal'))
    else:
        request.session['user_id'] = user[0].id
        return HttpResponseRedirect(reverse('banking_system:user_portal'))

def create_user(request):
    if not request.POST:
        return render(request, template_name='banking_app/create_user.html')
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO customer VALUES(%s,%s,%s,%s,%s)",
                       [request.POST['id'],request.POST['lname'],request.POST['fname'],
                        request.POST['email'],request.POST['address']])
        cursor.execute("INSERT INTO users VALUES(users_seq.nextval,%s,%s,0,%s)",
                       [request.POST['username'],request.POST['password'],
                        request.POST['id']])
        cursor.execute("INSERT INTO phonenumber VALUES(%s,%s)",
                       [request.POST['id'], request.POST['phone']])
        if request.POST['phone1']:
            cursor.execute("INSERT INTO phonenumber VALUES(%s,%s)",
                           [request.POST['id'], request.POST['phone1']])


    user = Users.objects.raw("SELECT * from users where username = %s AND password = %s",
                             [request.POST['username'], request.POST['password']])
    request.session['user_id'] = user[0].id
    return HttpResponseRedirect(reverse('banking_system:user_portal'))

def create_account(request):
    curr = list(Currency.objects.raw("SELECT abbreviation FROM currency"))
    curr = [i.abbreviation for i in curr]
    types = list(Accounttype.objects.raw("SELECT * FROM accounttype"))
    types = [i.name for i in types]
    if not request.POST:
        return render(request,"banking_app/create_account.html",context={
            'curr': curr,
            'types': types,
        })
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO account VALUES(account_seq.next_val,%s,%s,%s,%s)",
                       [request.POST['account_type'], request.POST['currency_type'], request.session['user_id'],
                        0])
        return HttpResponseRedirect(reverse('banking_system:user_portal'))


def user_portal(request):
    print(request.session['user_id'])
    return render(request,'banking_app/user_portal.html')

def adminPortal(request):
    print(request.session['user_id'])
    if not request.session['user_id']:
        return HttpResponseRedirect(reverse('banking_system:login'))
    user = list(Users.objects.raw("SELECT * from users where id=%s",
                             [request.session['user_id']]))
    if user[0].type==0:
        return HttpResponse("you are not allowed here!!! stop it!")
    return render(request, 'banking_app/adminPortal.html')

def manageAccounts(request):
    return HttpResponse("Managing Accounts.")

def manageAccountTypes(request):
    AccountTypes = Accounttype.objects.raw("SELECT * from accounttype")
    debit_interest = request.POST.get('Debit_interest', AccountTypes[0].interest)
    current_interest = request.POST.get('Current_interest', AccountTypes[1].interest)
    saving_interest = request.POST.get('Saving_interest', AccountTypes[2].interest)
    debit_ceiling = request.POST.get('Debit_ceiling', AccountTypes[0].ceiling)
    current_ceiling = request.POST.get('Current_ceiling', AccountTypes[1].ceiling)
    saving_ceiling = request.POST.get('Saving_ceiling', AccountTypes[2].ceiling)
    
    with connection.cursor() as c:
         c.execute("UPDATE accounttype SET ceiling = " + str(debit_ceiling) + ", interest = " + str(debit_interest) + " WHERE name = 'Debit'")
         c.execute("UPDATE accounttype SET ceiling = " + str(current_ceiling) + ", interest = " + str(current_interest) + " WHERE name = 'Current'")
         c.execute("UPDATE accounttype SET ceiling = " + str(saving_ceiling) + ", interest = " + str(saving_interest) + " WHERE name = 'Saving'")
    
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

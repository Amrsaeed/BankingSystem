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
    customer_id = list(Users.objects.raw("SELECT * FROM users WHERE id=%s",
                                        [request.session['user_id']]))[0].customerid.customerid
    if not request.POST:
        return render(request,"banking_app/create_account.html",context={
            'curr': curr,
            'types': types,
        })
    # print([request.POST['account_type'], request.POST['currency_type'], account_id])
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO account VALUES(account_seq.nextval,%s,%s,%s,0)",
                       [request.POST['account_type'], request.POST['currency_type'], customer_id])
        return HttpResponseRedirect(reverse('banking_system:user_portal'))


def user_portal(request):
    request.session['account_num'] = None
    customer_id = list(Users.objects.raw("SELECT * FROM users WHERE id=%s",
                                         [request.session['user_id']]))[0].customerid.customerid
    accounts = list(Account.objects.raw("SELECT * FROM account WHERE customerid=%s", [customer_id]))
    if not request.POST:
        return render(request,'banking_app/user_portal.html',context={
            'accs' : accounts,
        })
    request.session['account_num'] = request.POST['account']

    if request.POST['action'] == 'Withdraw':
        return HttpResponseRedirect(reverse('banking_system:withdraw'))
    elif request.POST['action'] == 'Deposit':
        return HttpResponseRedirect(reverse('banking_system:deposit'))
    elif request.POST['action'] == 'Transfer':
        return HttpResponseRedirect(reverse('banking_system:transfer'))
    else:
        return HttpResponseRedirect(reverse('banking_system:summary'))

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
    if request.POST.get('edit') == 'Edit':
       editCustomer(request)
       customer = Customer.objects.raw("SELECT * from customer WHERE customerid = " + request.POST.get('customer_id', -1))
       context = {'CustomerID': customer[0].customerid, 'Fname': customer[0].fname, 'Lname': customer[0].lname, 'Address': customer[0].address, 'Email': customer[0].email,}
       return render(request, 'banking_app/edit_customer.html', context)
    
    if request.POST.get('add') == 'Add Customer':
       return render(request, 'banking_app/add_customer.html')
       
    customers = Customer.objects.raw("SELECT * from customer")
    context = {'Customers': customers,}
    return render(request, 'banking_app/manage_customers.html', context)

def summary(request):
    print(request.session['account_num'])
    acc = list(Account.objects.raw("SELECT * FROM account WHERE accountnum=%s",
                                   [request.session['account_num']]))[0]
    trans = list(Transaction.objects.raw("SELECT * FROM transaction WHERE accountnum =%s",
                                         [request.session['account_num']]))
    print(acc)
    print(trans)
    return render(request,'banking_app/summary.html',context={
        'acc':acc,
        'trans': trans,
    })

def withdraw(request):
    return HttpResponse("Withdraw money.")

def deposit(request):
    return HttpResponse("deposit money.")

def transfer(request):
    return HttpResponse("Transfer money.")
    
def editCustomer(request):
    customerID = request.POST.get('customer_id', 0)
    customerFname = request.POST.get('customer_fname', 0)
    customerLname = request.POST.get('customer_lname', 0)
    customerEmail = request.POST.get('customer_email', 0)
    customerAddress = request.POST.get('customer_address', 0)
    print(customerID, customerFname, customerLname, customerEmail, customerAddress)
    with connection.cursor() as c:
        c.execute("UPDATE customer SET fname = '" + str(customerFname) + "' WHERE customerid = " + str(customerID))
        c.execute("UPDATE customer SET lname = '" + str(customerLname) + "' WHERE customerid = " + str(customerID))
        c.execute("UPDATE customer SET email = '" + str(customerEmail) + "' WHERE customerid = " + str(customerID))
        c.execute("UPDATE customer SET address = '" + str(customerAddress) + "' WHERE customerid = " + str(customerID))

    context = {'CustomerID': customerID, 'Fname': customerFname, 'Lname': customerLname, 'Address': customerAddress, 'Email': customerEmail,}
    return render(request, 'banking_app/edit_customer.html', context)
	
def addCustomer(request):
    customerID = request.POST.get('customer_id', 0)
    customerFname = request.POST.get('customer_fname', '')
    customerLname = request.POST.get('customer_lname', '')
    customerEmail = request.POST.get('customer_email', '')
    customerAddress = request.POST.get('customer_address', '')
    with connection.cursor() as c:
        c.execute("SELECT COUNT(*) from customer")
        customerid = c.fetchone()
        customerid = customerid[0] + 1
        c.execute("INSERT INTO customer (customerid, fname, lname, email, address) VALUES (" + str(customerid) + ",'" + customerFname + "', '" + customerLname + "', '" + customerEmail + "', '" + customerAddress + "')")
    context = {'CustomerID': customerID, 'Fname': customerFname, 'Lname': customerLname, 'Address': customerAddress, 'Email': customerEmail,}
    return render(request, 'banking_app/add_customer.html', context)

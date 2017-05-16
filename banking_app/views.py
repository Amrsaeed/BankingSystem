from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.db import connection
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

def accountSummary(request):
    return HttpResponse("User account summary.")

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

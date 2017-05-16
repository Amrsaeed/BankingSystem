from django.conf.urls import url

from . import views

app_name = 'banking_system'
urlpatterns = [
    url(r'^$', views.login_page, name='login_page'),
    url(r'^login_process/$', views.login, name='login'),
    url(r'^createUser/$', views.createUser, name='createUser'),
    url(r'^createAccount/$', views.createAccount, name='createAccount'),
    url(r'^userPortal/$', views.userPortal, name='userPortal'),
    url(r'^adminPortal/$', views.adminPortal, name='adminPortal'),
    url(r'^adminPortal/manageCustomers/$', views.manageCustomers, name='manageCustomers'),
    url(r'^adminPortal/manageCustomers/editCustomer$', views.editCustomer, name='editCustomer'),
    url(r'^adminPortal/manageCustomers/addCustomer$', views.addCustomer, name='addCustomer'),
    url(r'^adminPortal/manageAccounts/$', views.manageAccounts, name='manageAccounts'),
    url(r'^adminPortal/manageAccountTypes/$', views.manageAccountTypes, name='manageAccountTypes'),
    url(r'^userPortal/accountSummary/$', views.accountSummary, name='accountSummary'),
    url(r'^userPortal/withdraw/$', views.withdraw, name='withdraw'),
    url(r'^userPortal/deposit/$', views.deposit, name='deposit'),
    url(r'^userPortal/transfer$', views.transfer, name='transfer'),
]

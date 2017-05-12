from django.conf.urls import url

from . import views

app_name = 'banking_system'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^createAccount/$', views.createAccount, name='createAccount'),
    url(r'^userPortal/$', views.userPortal, name='userPortal'),
    url(r'^adminPortal/$', views.adminPortal, name='adminPortal'),
    url(r'^adminPortal/manageCustomers/$', views.manageCustomers, name='manageCustomers'),
    url(r'^adminPortal/manageAccounts/$', views.manageAccounts, name='manageAccounts'),
    url(r'^adminPortal/manageAccountTypes/$', views.manageAccountTypes, name='manageAccountTypes'),
    url(r'^manageCustomers/$', views.manageCustomers, name='manageCustomers'),
    url(r'^userPortal/accountSummary/$', views.accountSummary, name='accountSummary'),
    url(r'^userPortal/withdraw/$', views.withdraw, name='withdraw'),
    url(r'^userPortal/deposit/$', views.deposit, name='deposit'),
    url(r'^userPortal/transfer$', views.transfer, name='transfer'),
]

from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Account)
admin.site.register(Accounttype)
admin.site.register(Currency)
admin.site.register(Customer)
admin.site.register(Phonenumber)
admin.site.register(Transaction)

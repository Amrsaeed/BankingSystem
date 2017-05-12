from django.db import models
from __future__ import unicode_literals
# Create your models here.


class Account(models.Model):
    accountnum = models.IntegerField(primary_key=True)
    accounttype = models.ForeignKey('Accounttype', models.DO_NOTHING, db_column='accounttype', blank=True, null=True)
    currency = models.ForeignKey('Currency', models.DO_NOTHING, db_column='currency', blank=True, null=True)
    customerid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customerid', blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'


class Accounttype(models.Model):
    name = models.CharField(primary_key=True, max_length=10)
    ceiling = models.IntegerField()
    interest = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounttype'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Currency(models.Model):
    abbreviation = models.CharField(primary_key=True, max_length=3)

    class Meta:
        managed = False
        db_table = 'currency'


class Customer(models.Model):
    customerid = models.IntegerField(primary_key=True)
    lname = models.CharField(max_length=10)
    fname = models.CharField(max_length=10)
    email = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Phonenumber(models.Model):
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customerid', primary_key=True)
    phonenum = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'phonenumber'
        unique_together = (('customerid', 'phonenum'),)


class Transaction(models.Model):
    transnum = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=1)
    transdate = models.DateField()
    amount = models.IntegerField()
    accountnum = models.ForeignKey(Account, models.DO_NOTHING, db_column='accountnum')

    class Meta:
        managed = False
        db_table = 'transaction'

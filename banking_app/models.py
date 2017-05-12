# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Account(models.Model):
    accountnum = models.IntegerField(primary_key=True)
    accounttype = models.ForeignKey('Accounttype', models.DO_NOTHING, db_column='accounttype', blank=True, null=True)
    currency = models.ForeignKey('Currency', models.DO_NOTHING, db_column='currency', blank=True, null=True)
    customerid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customerid', blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'


class Accounttype(models.Model):
    name = models.CharField(primary_key=True, max_length=10)
    ceiling = models.FloatField()
    interest = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounttype'


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
    amount = models.FloatField()
    accountnum = models.ForeignKey(Account, models.DO_NOTHING, db_column='accountnum')

    class Meta:
        managed = False
        db_table = 'transaction'

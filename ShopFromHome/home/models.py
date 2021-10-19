from django.db import models
from django.contrib.auth.hashers import *


# Create your models here.

class Shopkeeper(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    contactNum = models.CharField(max_length=10, verbose_name="Phone Number")
    resAddress = models.TextField(verbose_name="Residential Address")
    shopName = models.CharField(max_length=100, verbose_name="Shop Name")
    shopAddress = models.TextField(verbose_name="Shop Address")
    password = models.CharField(max_length=30, verbose_name="Password")

    def __str__(self):
        return self.name + " -> " + self.email


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    contactNum = models.CharField(max_length=10, verbose_name="Phone Number")
    deliveryAddress = models.TextField(verbose_name="Delivery Address")
    password = models.CharField(max_length=30, verbose_name="Password")

    def __str__(self):
        return self.name + " -> " + self.email

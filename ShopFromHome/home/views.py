from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Customer, Shopkeeper

from home.models import Shopkeeper


# Create your views here.


def shopHome(request):
    return render(request, "shopHome.html")


def customerSignUp(request):
    if request.method == 'POST':
        name = request.POST['fullName']
        email = request.POST['signEmail']
        number = request.POST['phoneNum']
        address = request.POST['residentialAddress']
        password = request.POST['signPassword']
        confirm_password = request.POST['cSignPassword']

        if len(name) < 3 or len(number) < 10:
            # Message
            return redirect('ShopHome')
        if password != confirm_password:
            # Message
            return redirect('ShopHome')

        customer = Customer.objects.create(name=name, email=email, contactNum=number, deliveryAddress=address,
                                           password=password)
        # Message
        return redirect('ShopHome')


def shopkeeperSignUp(request):
    if request.method == 'POST':
        name = request.POST['fullName']
        email = request.POST['signEmail']
        number = request.POST['phoneNum']
        address = request.POST['residentialAddress']
        shop_name = request.POST['shopName']
        shop_address = request.POST['shopAddress']
        password = request.POST['signPassword']
        confirm_password = request.POST['cSignPassword']

        if len(name) < 3 or len(number) < 10:
            # Message
            return redirect('ShopHome')
        if password != confirm_password:
            # Message
            return redirect('ShopHome')

        shopkeeper = Shopkeeper.objects.create(name=name, email=email, contactNum=number, resAddress=address,
                                               shopName=shop_name, shopAddress=shop_address, password=password)
        # Message
        return redirect('ShopHome')


def shopkeeperLogin(request):
    if request.method == "POST":
        email = request.POST['linEmailId']
        password = request.POST['linPassword']

        shopkeeper = Shopkeeper.objects.get(email=email)
        if shopkeeper.password == password:
            shopkeeper_id = shopkeeper.id
            return redirect('shopkeeperHome')


def customerLogin(request):
    if request.method == "POST":
        email = request.POST['linEmailId']
        password = request.POST['linPassword']

        customer = Customer.objects.get(email=email)
        if customer.password == password:
            shopkeeper_id = customer.id
            return redirect('customerHome')


def shopkeeperHome(request):
    return render(request, "shopkeeperHome.html")


def customerHome(request):
    return render(request, "customerHome.html")


def shopkeeperLogout(request):
    logout(request)
    return HttpResponseRedirect("/shopkeeperLogin")

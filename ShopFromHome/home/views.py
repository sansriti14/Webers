from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from home.models import Shopkeeper

# Create your views here.


def index(request):
    return render(request, "index.html")


def shopkeeperSignup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        shop = request.POST['shop']
        if len(request.FILES) != 0:
            image = request.FILES['image']
        user = User.objects.create_user(name, email, password)
        shopkeeper = Shopkeeper(name=name, shop=shop,
                                email=email, phone=phone, image=image)
        shopkeeper.save()

    return render(request, "shopkeeperSignup.html")


def shopkeeperLogin(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/shopkeeperHome")
        else:
            return HttpResponseRedirect("/shopkeeperLogin")

    return render(request, "shopkeeperLogin.html")


def shopkeeperHome(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/shopkeeperLogin")
    return render(request, "shopkeeperHome.html")


def shopkeeperLogout(request):
    logout(request)
    return HttpResponseRedirect("/shopkeeperLogin")

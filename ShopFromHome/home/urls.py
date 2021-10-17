from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shopkeeperSignup", views.shopkeeperSignup, name="shopkeeperSignup"),
    path("shopkeeperLogin", views.shopkeeperLogin, name="shopkeeperLogin"),
    path("shopkeeperHome", views.shopkeeperHome, name="shopkeeperHome"),
    path("shopkeeperLogout", views.shopkeeperLogout, name="shopkeeperLogout"),
]

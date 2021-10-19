from django.urls import path
from home import views

urlpatterns = [
    path("", views.shopHome, name="ShopHome"),
    path("customerSignUp/", views.customerSignUp, name="customerSignUp"),
    path("shopkeeperSignUp/", views.shopkeeperSignUp, name="shopkeeperSignUp"),
    path("shopkeeperLogin/", views.shopkeeperLogin, name="shopkeeperLogin"),
    path("varShopkeeperHome/", views.shopkeeperHome, name="shopkeeperHome"),
    path("customerLogin/", views.customerLogin, name="customerLogin"),
    path("varCustomerHome/", views.customerHome, name="customerHome"),

]

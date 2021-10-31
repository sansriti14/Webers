from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING, RESTRICT
from django.utils import timezone

# Create your models here.

# For details of shopkeeper
class Shopkeeper(models.Model):
    name = models.CharField(max_length=1000)
    shop = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = models.IntegerField()
    image = models.ImageField(upload_to="shops/images", blank=True, null=True)

    def __str__(self):
        return self.name

# For reqeusts of customer
class Requests(models.Model):
    name = models.CharField(max_length=1000)
    item = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    type = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    receive = models.IntegerField(default=0)

# For checking if shopkeeper has responded to a request
class HasResponded(models.Model):
    name = models.CharField(max_length=1000)
    req = models.ForeignKey(Requests, on_delete=CASCADE)

# For details of items of a shopkeeper
class Items(models.Model):
    name = models.CharField(max_length=1000)
    item = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    price = models.IntegerField()

# For responses of shopkeeper
class Responses(models.Model):
    name = models.CharField(max_length=1000)
    shop = models.CharField(max_length=1000)
    price = models.IntegerField()
    req = models.ForeignKey(Requests, on_delete=CASCADE, null=True)
    date = models.DateField(default=timezone.now)

# For record of past orders of customer
class PastOrders(models.Model):
    name = models.CharField(max_length=1000)
    shop = models.CharField(max_length=1000)
    shopkeeper = models.CharField(max_length=1000)
    item = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    price = models.IntegerField()
    date = models.DateField()
    returnItem = models.BooleanField(default=False)
    reason = models.TextField(null=True)

# For record of sales of shopkeeper
class RecordForShopkeeper(models.Model):
    customer = models.CharField(max_length=1000)
    shop = models.CharField(max_length=1000, null=True)
    shopkeeper = models.CharField(max_length=1000, null=True)
    item = models.CharField(max_length=1000, null=True)
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    date = models.DateField(null=True)

# For reviews of shops and items
class Comments(models.Model):
    name = models.CharField(max_length=1000)
    comment = models.TextField()
    shop = models.ForeignKey(Shopkeeper, on_delete=CASCADE, null=True)
    item = models.ForeignKey(Items, on_delete=CASCADE, null=True)

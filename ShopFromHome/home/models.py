from django.db import models

# Create your models here.


class Shopkeeper(models.Model):
    name = models.CharField(max_length=1000)
    shop = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = models.IntegerField()
    image = models.ImageField(upload_to="shops/images", blank=True, null=True)

    def __str__(self):
        return self.name

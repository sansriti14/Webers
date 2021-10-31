from django.contrib import admin

from home.models import Comments, HasResponded, Items, PastOrders, RecordForShopkeeper, Requests, Responses, Shopkeeper

# Register your models here.
admin.site.register(Shopkeeper)

admin.site.register(Requests)

admin.site.register(Items)

admin.site.register(Responses)

admin.site.register(HasResponded)

admin.site.register(PastOrders)

admin.site.register(RecordForShopkeeper)

admin.site.register(Comments)

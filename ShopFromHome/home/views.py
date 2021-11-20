from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from home.models import Customer, HasResponded, Items, PastOrders, Requests, Responses, Shopkeeper, Comments, RecordForShopkeeper

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
    res = Items.objects.filter(name=request.user.username)
    return render(request, "shopkeeperHome.html", {"res": res})


def shopkeeperLogout(request):
    logout(request)
    return HttpResponseRedirect("/shopkeeperLogin")


def customerHome(request):
    shops = Shopkeeper.objects.all()
    return render(request, "customerHome.html", {"shops": shops})


def broadcastRequest(request):
    if request.method == "POST":
        item = request.POST['item']
        quantity = request.POST['quantity']
        type = request.POST['orderType']
        req = Requests(name=request.user.username, item=item,
                       quantity=quantity, type=type)
        req.save()
    return HttpResponseRedirect("/customerHome")


def addItems(request):
    if request.method == "POST":
        item = request.POST['item']
        quantity = request.POST['quantity']
        price = request.POST['price']
        i = Items(name=request.user.username, item=item,
                  quantity=quantity, price=price)
        i.save()
    return HttpResponseRedirect("/shopkeeperHome")


def receivedRequests(request):
    reqs = Requests.objects.all()
    list = []
    for req in reqs:
        re = Items.objects.filter(name=request.user.username, item=req.item)
        if re.exists():
            if req.quantity <= re.first().quantity:
                if HasResponded.objects.filter(name=request.user.username, req=req).exists():
                    pass
                else:
                    req.price = re.first().price
                    req.save()
                    list.append(req)
    return render(request, "requests.html", {"list": list})


def sendResponse(request, id):
    if request.method == "POST":
        price = request.POST['price']
        req = Requests.objects.get(id=id)
        req.price = price
        req.receive += 1
        req.save()
        shop = Shopkeeper.objects.get(name=request.user.username).shop
        res = Responses(name=request.user.username, shop=shop,
                        price=price, req=req)
        res.save()
        responded = HasResponded(name=request.user.username, req=req)
        responded.save()
    return HttpResponseRedirect("/receivedRequests")


def receivedResponses(request):
    reqs = Requests.objects.filter(name=request.user.username)
    list = []
    for req in reqs:
        re = Items.objects.filter(item=req.item)
        if re.exists():
            if req.quantity <= re.first().quantity:
                list.append(req)
    responses = []
    for req in list:
        response = []
        res = Responses.objects.filter(req=req)
        if res.first().req.type == "manual":
            for r in res:
                response.append(r)
        elif res.first().req.type == "automatic":
            price = res.first().price
            for r in res:
                if r.price < price:
                    price = r.price
            for r in res:
                if r.price == price:
                    response.append(r)
                    break
        responses.append(response)
    return render(request, "response.html", {"responses": responses})


def acceptResponse(request, resid, reqid):
    res = Responses.objects.get(id=resid)
    req = Requests.objects.get(id=reqid)
    item = Items.objects.get(name=res.name, item=req.item)
    item.quantity -= req.quantity
    order = PastOrders(name=request.user.username, shop=res.shop,
                       shopkeeper=res.name, item=req.item, quantity=req.quantity, price=res.price, date=res.date)
    order.save()
    record = RecordForShopkeeper(
        customer=req.name, shop=res.shop, shopkeeper=res.name, item=req.item, quantity=req.quantity, price=res.price, date=res.date)
    record.save()
    item.save()
    req.delete()
    return HttpResponseRedirect("/receivedResponses")


def pastOrders(request):
    res = PastOrders.objects.filter(
        name=request.user.username, returnItem=False)
    return render(request, "pastOrders.html", {"res": res})


def returnOrder(request, id):
    if request.method == "POST":
        res = PastOrders.objects.get(id=id)
        res.returnItem = True
        reason = request.POST['reason']
        res.reason = reason
        res.save()
    return HttpResponseRedirect("/pastOrders")


def returnRequests(request):
    res = PastOrders.objects.filter(
        shopkeeper=request.user.username, returnItem=True)
    print(res)
    return render(request, "returnRequests.html", {"res": res})


def acceptReturn(request, id):
    res = PastOrders.objects.get(id=id)
    item = Items.objects.get(name=res.shopkeeper, item=res.item)
    item.quantity += res.quantity
    item.save()
    res.delete()
    return HttpResponseRedirect("/returnRequests")

# For maintaining sales records by shopkeeper


def records(request):
    res = RecordForShopkeeper.objects.filter(
        shopkeeper=request.user.username)
    return render(request, "record.html", {"res": res})

# For maintaining record of unavailable items


def unavailable(request):
    res = Requests.objects.filter(name=request.user.username, receive=0)
    return render(request, "unavailable.html", {"res": res})

# For searching records in shopkeeper sales records


def searchRecords(request):
    if request.method == "POST":
        search = request.POST['search']
        if search != "":
            res = RecordForShopkeeper.objects.filter(
                shopkeeper=request.user.username, customer=search)
            if len(res) != 0:
                return render(request, "searchRecords.html", {"res": res})
            record = RecordForShopkeeper.objects.filter(
                shopkeeper=request.user.username, item=search)
            return render(request, "searchRecords.html", {"res": record})
        return HttpResponseRedirect("/records")

# For getting all items of a shopkeeper


def enterShop(request, id):
    shop = Shopkeeper.objects.get(id=id)
    items = Items.objects.filter(name=shop.name)
    return render(request, "items.html", {"items": items, "shopId": id})

# For submitting review about a shop by customer


def submitComments(request, id):
    shop = Shopkeeper.objects.get(id=id)
    if request.method == "POST":
        comment = request.POST['comment']
        entry = Comments(name=request.user.username,
                         comment=comment, shop=shop)
        entry.save()
    return HttpResponseRedirect("http://127.0.0.1:8000/customerHome")

# For getting all reviews about a particular shop


def shopComments(request, id):
    shop = Shopkeeper.objects.get(id=id)
    comments = Comments.objects.filter(shop=shop)
    return render(request, "shopComments.html", {"comments": comments})

# For submitting review about an item by customer


def submitReviews(request, shopId, itemId):
    item = Items.objects.get(id=itemId)
    shop = Shopkeeper.objects.get(id=shopId)
    if request.method == "POST":
        comment = request.POST['comment']
        com = Comments(name=request.user.username,
                       comment=comment, shop=shop, item=item)
        com.save()
        return HttpResponseRedirect("http://127.0.0.1:8000/"+str(shopId)+"/enterShop")

# For getting all reviews about a particular shop


def itemReviews(request, shopId, itemId):
    item = Items.objects.get(id=itemId)
    shop = Shopkeeper.objects.get(id=shopId)
    res = Comments.objects.filter(item=item, shop=shop)
    return render(request, "itemReviews.html", {"res": res})

# For customer signup


def customerSignup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        user = User.objects.create_user(name, email, password)
    return render(request, "customerSignup.html")

# For customer login


def customerLogin(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/customerHome")
        else:
            return HttpResponseRedirect("/customerLogin")

    return render(request, "customerLogin.html")


# For customer logout
def customerLogout(request):
    logout(request)
    return HttpResponseRedirect("/customerLogin")


# def addItem(request):
#     if request.method == "POST":
#         name = request.POST['ItemName']
#         qty = request.POST['ItemQty']
#         price = request.POST['ItemPrice']
#         image_url = request.POST['ItemImage']
#         item = Items.objects.create(
#             item=name, quantity=qty, price=price, name=request.user.username)
#     return HttpResponseRedirect("/shopkeeperHome")


# def searchItem(request, shopkeeper_id):
#     if request.method == "POST":
#         item_name = request.POST['ItemName']
#         shopkeeper = Shopkeeper.objects.get(pk=shopkeeper_id)
#         item = Items.objects.filter(shopkeeper=shopkeeper).filter(
#             name__icontains=item_name)

#         if item:
#             item_found = item[0]
#             response = "Item Found -> " + str(item_found)
#             return HttpResponse(response)
#         else:
#             return HttpResponse("Not Found")


def updateItem(request):
    if request.method == 'POST':
        item_id = request.POST['ItemId']
        new_qty = request.POST['NewQty']
        new_price = request.POST['NewPrice']
        new_image = request.POST['NewImage']

        # shopkeeper = Shopkeeper.objects.get(pk=shopkeeper_id)

        item = Items.objects.get(pk=item_id, name=request.user.username)

        if int(new_qty) > 0:
            item.quantity = new_qty
            item.save()

        if float(new_price) > 0:
            item.price = new_price
            item.save()

        if new_image != "https://www.blank.com/":
            item.image_link = new_image
            item.save()

    return HttpResponseRedirect("/shopkeeperHome")


def deleteItem(request, shopkeeper_id):
    if request.method == 'POST':
        item_id = request.POST['ItemId']

        # shopkeeper = Shopkeeper.objects.get(pk=shopkeeper_id)

        item = Items.objects.get(pk=item_id, name=request.user.username)
        item.delete()

    return HttpResponseRedirect("/shopkeeperHome")


# def openShop(request, customer_id):
#     if request.method == 'POST':
#         shop_id = request.POST['ShopId']
#         shopkeeper = Shopkeeper.objects.get(pk=shop_id)

#         shop_items = Items.objects.filter(shopkeeper=shopkeeper)
#         customer = Customer.objects.get(pk=customer_id)

#         context = {
#             'shopkeeper': shopkeeper,
#             'customer': customer,
#             'all_items': shop_items,
#         }

#         return render(request, "sfrmcside.html", context=context)


# def searchItem(request, customer_id):
#     if request.method == 'POST':
#         item_name = request.POST['ItemName']
#         shop_id = request.POST['ShopId']

#         shopkeeper = Shopkeeper.objects.get(pk=shop_id)

#         items_found = Items.objects.filter(
#             shopkeeper=shopkeeper).filter(name__icontains=item_name)
#         customer = Customer.objects.get(pk=customer_id)

#         context = {
#             'shopkeeper': shopkeeper,
#             'customer': customer,
#             'all_items': items_found,
#         }

#         return render(request, "sfrmcside.html", context=context)


# def orderItem(request, customer_id):
#     if request.method == 'POST':
#         item_id = request.POST['ItemId']
#         shop_id = request.POST['ShopId']
#         order_qty = request.POST['Qty']

#         shopkeeper = Shopkeeper.objects.get(pk=shop_id)
#         shopkeeper_name = shopkeeper.name
#         shop_name = shopkeeper.shopName
#         item = Items.objects.get(pk=item_id, shopkeeper=shopkeeper)
#         customer = Customer.objects.get(pk=customer_id)
#         customer_name = customer.name
#         shop_items = Items.objects.filter(shopkeeper=shopkeeper)

#         if 0 < int(order_qty) <= int(item.quantity):
#             order = PastOrders.objects.create(name=customer_name, shopkeeper=shopkeeper_name, shop=shop_name, item=item.name,
#                                               price=item.price, quantity=order_qty, date=timezone.now())
#             item.quantity -= int(order_qty)
#             item.save()

#             context = {
#                 'shopkeeper': shopkeeper,
#                 'customer': customer,
#                 'all_items': shop_items,
#             }

#             # message
#             return render(request, "sfrmcside.html", context=context)
#         else:
#             response = "Invalid Quantity, Order Unsuccessful"
#             return HttpResponse(response)

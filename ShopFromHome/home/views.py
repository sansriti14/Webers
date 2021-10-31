from django import shortcuts
from django.db.models import query
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from home.models import Comments, HasResponded, Items, PastOrders, RecordForShopkeeper, Requests, Responses, Shopkeeper

# Create your views here.

# For front page
def index(request):
    return render(request, "index.html")

# For shopkeeper signup
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

# For shopkeeper login
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

# For home page of shopkeeper
def shopkeeperHome(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/shopkeeperLogin")
    return render(request, "shopkeeperHome.html")

# For shopkeeper logout
def shopkeeperLogout(request):
    logout(request)
    return HttpResponseRedirect("/shopkeeperLogin")

# For home page of customer
def customerHome(request):
    shops = Shopkeeper.objects.all()
    return render(request, "customerHome.html", {"shops": shops})

# For broadcasting a request by customer
def broadcastRequest(request):
    if request.method == "POST":
        item = request.POST['item']
        quantity = request.POST['quantity']
        type = request.POST['orderType']
        req = Requests(name=request.user.username, item=item,
                       quantity=quantity, type=type)
        req.save()
    return HttpResponseRedirect("/customerHome")

# For adding items by shopkeeper
def addItems(request):
    if request.method == "POST":
        item = request.POST['item']
        quantity = request.POST['quantity']
        price = request.POST['price']
        i = Items(name=request.user.username, item=item,
                  quantity=quantity, price=price)
        i.save()
    return HttpResponseRedirect("/shopkeeperHome")

# For receiving requests by shopkeeper
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
                    req.receive += 1
                    req.save()
                    list.append(req)
    return render(request, "requests.html", {"list": list})

# For sending response by shopkeeper
def sendResponse(request, id):
    if request.method == "POST":
        price = request.POST['price']
        req = Requests.objects.get(id=id)
        req.price = price
        shop = Shopkeeper.objects.get(name=request.user.username).shop
        res = Responses(name=request.user.username, shop=shop,
                        price=price, req=req)
        res.save()
        responded = HasResponded(name=request.user.username, req=req)
        responded.save()
    return HttpResponseRedirect("http://127.0.0.1:8000/receivedRequests")

# For receiving responses by customer
def receivedResponses(request):
    list = Requests.objects.filter(name=request.user.username)
    responses = []
    for req in list:
        response = []
        res = Responses.objects.filter(req=req)
        if len(res) != 0:
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

# For accepting response by customer
def acceptResponse(request, resid, reqid):
    res = Responses.objects.get(id=resid)
    req = Requests.objects.get(id=reqid)
    item = Items.objects.get(name=res.name, item=req.item)
    item.quantity -= req.quantity
    order = PastOrders(name=request.user.username, shop=res.shop,
                       shopkeeper=res.name, item=req.item, quantity=req.quantity, price=res.price, date=res.date)
    order.save()
    record = RecordForShopkeeper(customer=request.user.username, shop=res.shop,
                                 shopkeeper=res.name, item=req.item, quantity=req.quantity, price=res.price, date=res.date)
    record.save()
    item.save()
    req.delete()
    return HttpResponseRedirect("/receivedResponses")

# For maintaining past orders of customer
def pastOrders(request):
    res = PastOrders.objects.filter(
        name=request.user.username, returnItem=False)
    return render(request, "pastOrders.html", {"res": res})

# For sending return request by customer
def returnOrder(request, id):
    res = PastOrders.objects.get(id=id)
    if request.method == "POST":
        reason = request.POST['reason']
        res.reason = reason
        res.returnItem = True
        res.save()
    return HttpResponseRedirect("/pastOrders")

# For receiving return requests by shopkeeper
def returnRequests(request):
    res = PastOrders.objects.filter(
        shopkeeper=request.user.username, returnItem=True)
    print(res)
    return render(request, "returnRequests.html", {"res": res})

# For accepting return requests by shopkeeper
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

# For getting all reviews about a particular item
def itemReviews(request, shopId, itemId):
    item = Items.objects.get(id=itemId)
    shop = Shopkeeper.objects.get(id=shopId)
    res = Comments.objects.filter(item=item, shop=shop)
    return render(request, "itemReviews.html", {"res": res})

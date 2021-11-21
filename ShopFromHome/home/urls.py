from django.urls import path
from home import views

urlpatterns = [
    # For front page
    path("", views.index, name="index"),

    # For shopkeeper signup
    path("shopkeeperSignup", views.shopkeeperSignup, name="shopkeeperSignup"),

    # For shopkeeper login
    path("shopkeeperLogin", views.shopkeeperLogin, name="shopkeeperLogin"),

    # For home page of shopkeeper
    path("shopkeeperHome", views.shopkeeperHome, name="shopkeeperHome"),

    # For shopkeeper logout
    path("shopkeeperLogout", views.shopkeeperLogout, name="shopkeeperLogout"),

    # For broadcasting a request by customer
    path("broadcastRequest", views.broadcastRequest, name="broadcastRequest"),

    # For home page of customer
    path("customerHome", views.customerHome, name="customerHome"),

    # For adding items by shopkeeper
    path("addItems", views.addItems, name="addItems"),

    # For receiving requests by shopkeeper
    path("receivedRequests", views.receivedRequests, name="receivedRequests"),

    # For sending response by shopkeeper
    path("<int:id>/sendResponse", views.sendResponse, name="sendResponse"),

    # For receiving responses by customer
    path("receivedResponses", views.receivedResponses, name="receivedResponses"),

    # For accepting response by customer
    path("<int:resid>/<int:reqid>/acceptResponse",
         views.acceptResponse, name="acceptResponse"),

    # For maintaining past orders of customer
    path("pastOrders", views.pastOrders, name="pastOrders"),

    # For sending return request by customer
    path("<int:id>/returnOrder", views.returnOrder, name="returnOrder"),

    # For receiving return requests by shopkeeper
    path("returnRequests", views.returnRequests, name="returnRequests"),

    # For accepting return requests by shopkeeper
    path("<int:id>/acceptReturn", views.acceptReturn, name="acceptReturn"),

    # For maintaining sales records by shopkeeper
    path("records", views.records, name="records"),

    # For maintaining record of unavailable items
    path("unavailable", views.unavailable, name="unavailable"),

    # For searching records in shopkeeper sales records
    path("searchRecords", views.searchRecords, name="searchRecords"),

    # For getting all items of a shopkeeper
    path("<int:id>/enterShop", views.enterShop, name="enterShop"),

    # For submitting review about a shop by customer
    path("<int:id>/submitComments", views.submitComments, name="submitComments"),

    # For getting all reviews about a particular shop
    path("<int:id>/shopComments", views.shopComments, name="shopComments"),

    # For submitting review about an item by customer
    path("<int:shopId>/<int:itemId>/submitReviews",
         views.submitReviews, name="submitReviews"),

    # For getting all reviews about a particular item
    path("<int:shopId>/<int:itemId>/itemReviews",
         views.itemReviews, name="itemReviews"),

    # For customer signup
    path("customerSignup", views.customerSignup, name="customerSignup"),

    # For customer login
    path("customerLogin", views.customerLogin, name="customerLogin"),

    # For customer logout
    path("customerLogout", views.customerLogout, name="customerLogout"),

    #     path("<int:shopkeeper_id>/searchItem/",
    #          views.searchItem, name="searchItem"),
    path("updateItem",
         views.updateItem, name="updateItem"),
    path("<int:shopkeeper_id>/deleteItem",
         views.deleteItem, name="deleteItem"),
    path("<int:shopId>/<int:itemId>/buyItem", views.buyItem, name="buyItem"),
]

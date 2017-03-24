from django.shortcuts import render, redirect
from models import WishList, Item
from django.contrib import messages
from ..log_reg.models import Users

# Create your views here.
def index(request):
    if "current_user" not in request.session:
        messages.error(request, "Must be logged in to view this page.")
        return redirect("log_reg:index")

    curr_user = Users.objects.get(id=request.session["current_user"]["id"])

    context = {
    "other_items" : Item.objects.all(),
    "current_user" : curr_user
    }


    if WishList.objects.filter(user=curr_user):
        context["wishlist"] = WishList.objects.get(user=curr_user)
        context["other_items"] =  Item.objects.exclude(wish_list=curr_user.wishlist_by_user)


    return render(request, "wish_list/index.html", context)

def add_item(request):

    if "current_user" not in request.session:
        messages.error(request, "Must be logged in to view this page.")
        return redirect("log_reg:index")

    return render(request, "wish_list/add_item.html")

def create_item(request, user_id):

    if "current_user" not in request.session:
        messages.error(request, "Must be logged in to view this page.")
        return redirect("log_reg:index")

    item_added = Item.objects.create_item(request.POST, user_id)

    if item_added[0]:
        return redirect("wish_list:index")
    else:
        for mes in item_added[1]:
            messages.error(request, mes)
        return redirect("wish_list:add_item")

def add_to_wishlist(request, user_id, item_id):

    if "current_user" not in request.session:
        messages.error(request, "Must be logged in to view this page.")
        return redirect("log_reg:index")

    user = Users.objects.get(id=user_id)
    item = Item.objects.get(id=item_id)
    try:
        wlist = WishList.objects.get(user=user)
    except:
        wlist = WishList.objects.create(user=user)

    wlist.items_by_wishlist.add(item)

    return redirect("wish_list:index")

def remove_from_wishlist(request, user_id, item_id):

    if "current_user" not in request.session:
        messages.error(request, "Must be logged in to view this page.")
        return redirect("log_reg:index")

    user = Users.objects.get(id=user_id)
    item = Item.objects.get(id=item_id)
    wlist = WishList.objects.get(user=user)
    wlist.items_by_wishlist.remove(item)

    return redirect("wish_list:index")

def delete_item(request, item_id):

    if "current_user" not in request.session:
        messages.error(request, "Must be logged in to view this page.")
        return redirect("log_reg:index")

    item = Item.objects.get(id=item_id).delete()

    return redirect("wish_list:index")

def item(request, item_id):

    if "current_user" not in request.session:
        messages.error(request, "Must be logged in to view this page.")
        return redirect("log_reg:index")

    context = {
    "item":Item.objects.get(id=item_id),
    "wishlists": WishList.objects.filter(items_by_wishlist=Item.objects.get(id=item_id))
    }

    return render(request, "wish_list/item.html", context)

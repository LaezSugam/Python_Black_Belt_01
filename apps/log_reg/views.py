from django.shortcuts import render, redirect
from django.contrib import messages
from models import Users

# Create your views here.
def index(request):

    return render(request, "log_reg/index.html")

def register(request):

    new_user = Users.objects.add_user(request.POST)

    if new_user[0]:
        request.session["current_user"] = {
        "id" : new_user[1].id,
        "name" : new_user[1].name,
        "username" : new_user[1].username
        }
        return redirect("log_reg:success")
    else:
        for mes in new_user[1]:
            messages.error(request, mes)
        return redirect("log_reg:index")

def login(request):

    new_user = Users.objects.login(request.POST)

    if new_user[0]:
        request.session["current_user"] = {
        "id" : new_user[1].id,
        "name" : new_user[1].name,
        "username" : new_user[1].username
        }
        return redirect("log_reg:success")
    else:
        messages.error(request, new_user[1])
        return redirect("log_reg:index")

def logout(request):

    del request.session["current_user"]

    return redirect("/")

def success(request):

    if "current_user" not in request.session:
        messages.error(request, "Must be logged in to view this page.")
        return redirect("log_reg:index")

    return render(request, "log_reg/success.html")

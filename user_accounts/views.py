from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from base.models import address, orders
from .forms import UserUpdateForm
from .models import *
from user_accounts.utils import *
from  django.http import HttpResponse

# Create your views here.

def success_view(request):

    return render(request, "success.html")



def view(request):

    user = request.user
    print(user)
    address_obj = address.objects.filter(host=user).first()

    orders_obj = orders.objects.filter(ordered_by=user)

    Customer_obj = customer.objects.filter(name = user).first()
    # checking whether reviews exists or not by the user
    Review = review.objects.filter(user = user)

    if Review :
      reviews = Customer_obj.activities.all()
    else :
        reviews = ""
    context = {
        "user": user,
        "address": address_obj,
        "orders": orders_obj,
        "customer":Customer_obj,
        "reviews" : reviews
    }
    return render(request, "user_profile.html", context)


def update_user(request):
    page = "update"
    user = request.user
    user_to_be_updated = User.objects.get(username=user.username)
    Customer = customer.objects.filter(name=user)
    form = UserUpdateForm(instance=user_to_be_updated)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_to_be_updated)
        if form.is_valid():
            old_username = user.username
            old_email = user.email
            form.save()

            if old_email == user.email:
                context = {"page": page, "a": old_email, "username": user.email}
                return render(request, "success.html", context)

            if old_username == user.username:
                send_email()
                context = {"page": page, "a": old_username, "username": user.username}
                return render(request, "success.html", context)

    return render(request, 'user_update.html', {'form': form, "customer": Customer})

def verify_email(request,pk):
    try:
        a = customer.objects.get(email_token = pk)
        a.email_is_verified = True
        a.save()
        return HttpResponse("your email has been verified")
    except:
         return Httpresponse("can't verify your email")


def delete_user(request):
    page = "delete"
    user = request.user
    user_to_be_delted = User.objects.get(username=user.username)
    
    if request.method == "POST":
        user_to_be_delted.delete()
        
    return render(request, "delete_user.html", {"user": user_to_be_delted, "page": page})

def delete_review(request):
    user = request.user
    Review = review.objects.get(user = user)
    context={
        "Review":Review
    }
    if request.method == "POST":

        Review.delete()


    return render(request,"delete_user.html")

def shippment_view(request):
    page = "shippment"
    user = request.user
    product = orders.objects.filter(ordered_by=user)
    shippment_status_list = []
    for prod in product:
        order_status = order_tracking.objects.filter(user=user, Product=prod.name).first()
        shippment_status_list.append(order_status)
    context = {

        "list" : shippment_status_list
    }

    return render(request , "order_details.html",context)


def shippment_details(request,pk):
    user = request.user
    product = orders.objects.filter(ordered_by = user)
    shippment_status_list = []
    for prod in product:
        order_status = order_tracking.objects.filter(user = user , Product = prod.name).first()
        shippment_status_list.append(order_status)

    for i in shippment_status_list:
        if i.Product.id == pk :
           return i
    a = i.dlivery_status.all()
    return render(request,"shippment_tracking.html",context={"a":a,"i":i})






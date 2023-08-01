from django.shortcuts import render
from django.contrib.auth.models import User
from base.models import address,orders
# Create your views here.


def view(request):
  
  user = User.objects.get(username = request.user.username)
  address_obj = address.objects.get(host = user)
  orders_obj = orders.objects.get(ordered_by = user)
  context = {
"user" : user,
"address" : address_obj,
"orders" : orders_obj

  }
  return render(request,"user_profile.html",context)
  

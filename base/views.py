from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import order_through_cart_form
from django.contrib.auth.decorators import login_required
import uuid
import datetime


def home(request):
    obj = product.objects.all()
    context = {'obj': obj}
    return render(request, 'home.html', context)


def user_accounts(request):
    return render(request, 'profile.html')


# user editting ( giving access to the user according to the authority)
# payment

def product_info(request, pk):
    count = 0
    obj = product.objects.get(id=pk)  # Use the correct Product model
    
    current_datetime = timezone.now()
    print(current_datetime)

    print(product.created_at ,"***********************************")
    two_days_later = current_datetime + datetime.timedelta(days=2)
    if obj.created_at > two_days_later:  # Use obj.created_at to access the creation date
        count = 1
    context = {'J': obj, "count": count}
    return render(request, 'PRODUCT-INFO.html', context)
# login/ log out user


def login_user(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('you are not a registered user')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect(home)


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:

            user = User.objects.create_user(
                username=username,
                password=password
            )

        #  User.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html')


@login_required(login_url='login-user')
def cart_items(request):
    user = request.user

    obj = cart.objects.filter(ordered_by=request.user)
    Product = product.objects.all()

    context = {'products': obj}

    return render(request, 'cart.html', context)


@login_required(login_url='login-user')
def add_item_to_cart(request, pk):
    user = request.user
    Product = product.objects.get(id=pk)
    cartItem = cart.objects.filter(item=Product, ordered_by=user)

    # context = {'product': product, 'cartItem': cartItem}

    if request.method == 'POST':
        if cartItem.exists():
            if Product.for_sale > 0:
                for item in cartItem:
                    item.quantity += 1
                    item.save()

            else:
                return HttpResponse('Sorry, the product is out of stock.')
        else:

            cartUpdate = cart.objects.create(ordered_by=user, item=Product)
            cartUpdate.save()

        return redirect('cart')


@login_required(login_url='login-user')
def cart_view(request):

    user = request.user
    cart_item = cart.objects.filter(ordered_by=user)

    context = {
        "cart_item": cart_item

    }
    return render(request, 'cart_view.html', context)


def delete_cart_item(request, pk):
    user = request.user
    Product = product.objects.get(id=pk)
    cart_items = cart.objects.filter(item=Product, ordered_by=user).first()
    #  if request.method == "POST":

    if cart_items.quantity == 1:
        cart_items.delete()
    else:
        cart_items.quantity -= 1
        cart_items.save()
    return redirect("cart")


@login_required(login_url='login-user')
def buy_now(request, pk):

    user = request.user
    Address = address.objects.get(host=user)
    Product = product.objects.get(id=pk)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity is not None and quantity.isdigit():  # Check if quantity is a valid number
            quantity = int(quantity)
            if Product.for_sale >= quantity:  # Ensure available quantity is sufficient
                Product.for_sale -= quantity
                Product.save()
                tracking_id = str(uuid.uuid4())[:8]
                total_amount = Product.price*quantity

                orders.objects.create(

                    name=Product,
                    ordered_by=user,
                    deliver_to=Address,
                    no_of_items=quantity,
                    total_amount=total_amount,
                    tracking_id=tracking_id
                )
                orders.save()

            else:
                return HttpResponse('Sorry, the requested quantity exceeds the available stock.')
        else:
            return HttpResponse('Please provide a valid quantity.')

        return redirect('cart_view')

    context = {'product': Product}
    return render(request, 'buy_now.html', context)


def buy_item_through_cart(request, pk):
    user = request.user
    Product = product.objects.get(id=pk)
    cart_item = cart.objects.filter(ordered_by=user, item=Product).first()
    # Initialize the form with the cart_item quantity
    tracking_id = str(uuid.uuid4())[:8]

    initial_data = {'amount': cart_item.quantity} if cart_item else {}
    form = order_through_cart_form(initial=initial_data)

    context = {
        'form': form
    }

    if request.method == 'POST':
        form = order_through_cart_form(request.POST)
        existing_tag = status.objects.get(name="DISPATCHED")
        if form.is_valid():

            # Create the order and update the product quantity
            order = orders.objects.create(
                ordered_by=user, name=Product, no_of_items=form.cleaned_data['amount'])
            Product.for_sale -= order.no_of_items
            Product.save()
            cart_item.delete()

            order_tracking.objects.create(
                tracking_id=tracking_id, user=user, Product=Product)
            order_tracking.dlivery_status.add(existing_tag)
            return redirect('cart')

    return render(request, 'buy_now_through_car.html', context)


def review_post(request, pk):
    try:
        Product = product.objects.get(id=pk)
    except product.DoesNotExist:
        return HttpResponse("Product not found.")

    obj = review.objects.filter(Product__name=Product)
    user = request.user
    Review = review.objects.filter(user=user)

    count = 0
    if not Review.exists():  # Check if the user has already submitted a review
        count = 1
    if request.method == "POST":
        rating = int(request.POST.get('rating', 0))
        if 0 < rating <= 5:  # Check if the rating is within the valid range
            Review = review.objects.create(user=user, body=request.POST.get(
                'review'), rating=rating, Product=Product)
            Review.save()
            # Redirect to the "info" page with the appropriate product's pk
            return redirect('info', pk=Product.pk)
        else:
            return HttpResponse("Please rate on the scale of 1 to 5.")

    context = {
        "obj": obj,
        "count": count
    }
    return render(request, "PRODUCT-INFO.html", context)


#  shippment tracking

def shippment_tracking(request, pk):
    order_item = orders.objects.get(id=pk)
    value = order_item.tracking_id
    shippmet_details = order_tracking.objects.filter(tracking_id=value).first()
    
    context = {"order_items": order_item}
    return render(request, "shippment_tracking.html", context)


#  notification

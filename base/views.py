from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from user_accounts.utils import *
from user_accounts.models import customer
# from base.search_bar_logic.services import *
import uuid
import datetime


# Assuming that category and product are classes defined in a module named models







def string_cleaner(string):
    cleaned_string = ""
    if string:
        if "," in string:
            for i in range(len(string)):
                if string[i] == ",":
                    continue
                cleaned_string += string[i]
        else:
            cleaned_string = string

        # Rest of the code remains unchanged
        c = []
        b = []
        Categories = category.objects.all()
        Products = product.objects.all()
        for cat in Categories:
            c.append(cat)
        for prod in Products:
            b.append(prod)

        a = ["500", "1000", "2000", "5000", "10000"]
        str1 = ""
        str2 = ""
        str3 = ""  # Initialize str3 to an empty string
        str4 = ""
        for price in a:
            if price in cleaned_string:
                str1 = price

        for i in b:
            if i.name in cleaned_string:
                str2 = (i.name)

            # Assuming 'name' is an attribute of the product instance
        for j in c:
            if j.name in cleaned_string:
                str3 = (j.name)
            # means "" is getting stored in str in case of no matching query
            # Assuming 'name' is an attribute of the category instance
            print(str1)
            print(str2)
            print(str3)
            # print(str1)

        if "above" in cleaned_string:
            str4 = "above"
        else:
            str4 = ""
        if "below" in cleaned_string:
            str4 = "below"
        else:
            str4 = ""
        return str1 + "," + str2 + "," + str3 + "," + str4
    else:
        return ""

# fl electro,dsadasdnics above 1000


def home(request):

    # Use the corrected string_cleaner function to clean the search query.

    q = request.GET.get("q")
    q = string_cleaner(q)

    print(q)

    # Initialize variables with default values
    p = ""
    t = ""
    s = ""
    r = ""

    # Split the cleaned string at the first comma (if present).

    if request.method == "POST":
        a = request.POST.get('button')
        if q:
            pass
    else:
        if q:
            # p : price
            # t : product
            # s : category
            # r : above or below
            p, t, s, r = q.split(",", 3)

    # If both s and r have values, use them for filtering the queryset.
        if r == "above":
            obj = product.objects.filter(
                name__istartswith=t[0:2], type__name__icontains=s, price__gt=int(p))
        elif r == "below":
            obj = product.objects.filter(
                name__istartswith=t[0:2], type__name__icontains=s, price__lte=int(p))
        else:
            obj = product.objects.filter(
                name__istartswith=t[0:2], type__name__icontains=s)
        #  just filter the results

    print(obj)
    context = {'obj': obj}
    return render(request, 'home.html', context)


# user editting ( giving access to the user according to the authority)
# payment

def product_info(request, pk):
    count = 0
    obj = product.objects.get(id=pk)  # Use the correct Product model
    review_obj = review.objects.filter(Product=obj)
    current_datetime = timezone.now()
    print(current_datetime)
    print(product.created_at, "***********************************")

    # Subtract two days from the current date
    two_days_ago = current_datetime - datetime.timedelta(days=2)

    if obj.created_at >= two_days_ago:
        count = 2
    reviewed_by_user = review.objects.filter(
        Product=obj, user=request.user).exists()

    context = {'J': obj, "obj": review_obj, "count": count,
               "reviewed_by_user": reviewed_by_user}
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
    user = request.user
    if request.method == 'POST':
        Address = request.POST.get("Address")
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:

            user = User.objects.create_user(
                username=username,
                password=password
            )
            a = address.objects.create(host=user,  name=Address)
            customer.objects.create(venue=a, name=user , email_token= str(uuid.uuid4()), email = email)
            send_email(email,customer.email_token)


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
    customer_instance = customer.objects.filter(name=user).first()
    address_instance = address.objects.filter(host=user).first()
    address_instance_ = address.objects.filter(host=user)
    product_instance = product.objects.get(id=pk)
    order_instance = orders.objects.filter(
        ordered_by=user, name=product_instance).first()
    order_item_in_customer_profile = customer_instance.Orders_till_now.all()
    count = 0
    


 

    if request.method == 'POST':
        existing_tag = status.objects.get(id=1)
        quantity = request.POST.get('quantity')
        print(quantity)
        # Replace 'address_field_name' with actual field name
        deliver_to = request.POST.get("address", address_instance)

        if quantity :
            quantity = int(quantity)
            if product_instance.for_sale >= quantity:
                product_instance.for_sale -= quantity
                product_instance.save()
                tracking_id = str(uuid.uuid4())[:8]
                total_amount = product_instance.price * quantity

                new_order = orders.objects.create(
                    name=product_instance,
                    ordered_by=user,
                    deliver_to=deliver_to,
                    no_of_items=quantity,
                    total_amount=total_amount
                )

                new_order.save()
                order_tracking_instance = order_tracking.objects.create(
                    tracking_id=tracking_id,
                    user=user,
                    Product=product_instance
                )

                order_tracking_instance.dlivery_status.add(existing_tag)
                order_tracking_instance.save()

                if customer_instance is None:
                    customer_instance = customer.objects.create(
                        name=user, venue=deliver_to)
                    customer_instance.save()

                if count == 0:
                    customer_instance.Orders_till_now.add(new_order)
                    customer_instance.save()

                # Redirect to a success page or some appropriate view
                return redirect('success-page')
            else:
                return HttpResponse('Sorry, the requested quantity exceeds the available stock.')
       

    # Render your template for displaying the form
    return render(request, 'buy_now.html', context={'product': product_instance,"name_":address_instance_})


def buy_item_through_cart(request, pk):
    user = request.user
    Customer = customer.objects.filter(name=user).first()
    Product = product.objects.get(id=pk)
    cart_item = cart.objects.filter(ordered_by=user, item=Product).first()
    Address = address.objects.filter(host=user).first()

    # Initialize the form with the cart_item quantity

    tracking_id = str(uuid.uuid4())[:8]

    initial_data = {'amount': cart_item.quantity} if cart_item else {}
    form = order_through_cart_form(initial=initial_data)

    context = {
        'form': form
    }

    if request.method == 'POST':
        form = order_through_cart_form(request.POST)
        existing_tag = status.objects.get(id=1)
        if form.is_valid():

            # Create the order and update the product quantity
            order = orders.objects.create(
                ordered_by=user, name=Product, no_of_items=form.cleaned_data['amount'])
            Product.for_sale -= order.no_of_items
            Product.save()
            if cart_item:
                cart_item.delete()

            a = order_tracking.objects.create(
                tracking_id=tracking_id, user=user, Product=Product)
            a.save()
            a.dlivery_status.add(existing_tag)
            a.save()

            if Customer is None:
                b = customer.objects.create(name=user, venue=Address)
                b.Orders_till_now.add(order)
                b.save()
            else:

                Customer = customer.objects.filter(name=user).first()

                Customer.Orders_till_now.add(order)
                Customer.save()

            return redirect('cart')

    return render(request, 'buy_now_through_car.html', context)


def review_post(request, pk):
    try:
        Product = product.objects.get(id=pk)
    except product.DoesNotExist:
        return HttpResponse("Product not found.")

    user = request.user
    Customer = customer.objects.filter(name=user).first()
    Review = review.objects.filter(user=user, Product=Product)

    if request.method == "POST" and Customer is not None:
        rating = int(request.POST.get('rating', 0))
        if 0 < rating <= 5:  # Check if the rating is within the valid range
            Review = review.objects.create(user=user, body=request.POST.get(
                'review'), rating=rating, Product=Product)
            Review.save()
            Customer.activities.add(Review)
            Customer.save()

            # Redirect to the "info" page with the appropriate product's pk
            return redirect('info', pk=Product.pk)
        else:
            return HttpResponse("Please rate on the scale of 1 to 5.")


def review_edit(request):
    user = request.user
    Reveiw = review.objects.get(user=user)
    form = review_edit_form(instance=Reveiw)

    if request.method == "POST":
        if form.is_valid():
            form = review_edit_form(request.post, instance=Reveiw)
            form.save()
    return render(request, "edit_review.html", {})


#  notification

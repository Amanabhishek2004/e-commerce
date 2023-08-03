
from django.contrib import admin
from django.urls import path , include
from . import views




urlpatterns = [
    path("",views.home,name="home"),
   
    path("register/", views.register_user, name="register-user"),
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'), 
    
    
    path('info/<str:pk>',views.product_info,name='info'),
    path("cart/",views.cart_view, name="cart"),

    path("accounts/", include('user_accounts.urls',namespace="accounts")),
    path("delete-cart/<str:pk>", views.delete_cart_item, name="delete_item"),
    path("add_to_cart/<str:pk>", views.add_item_to_cart, name="add_item"),
    path("buy_now/<str:pk>", views.buy_now, name="buy_item"),
    path("buy-item/<str:pk>",views.buy_item_through_cart, name="buy-item"),


    path("review/<str:pk>", views.review_post, name="review"),
    path("shippment-tracking/",views.shippment_tracking, name="tracking"),


]
from django.urls import path,include
from . import views

app_name = "accounts"

urlpatterns = [
    path("user-profile/",views.view , name="user-profile"),
    path("update-user/", views.update_user, name="update-user"),
    path("delete-user/",views.delete_user,name = "delete-user"),
    path('success/', views.success_view, name='success'),
    path("delete-review/",views.delete_review, name = "delete-review"),
    path("shippment-tracking/",views.shippment_view, name="tracking"),
    path("shippment-details/<str:pk>", views.shippment_details, name="details")

]

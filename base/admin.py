from django.contrib import admin
from .models import *


# # Register your models here.

admin.site.register(product)
admin.site.register(cart)
admin.site.register(category)
admin.site.register(address)
admin.site.register(orders)
admin.site.register(review)
admin.site.register(status)
admin.site.register(order_tracking)




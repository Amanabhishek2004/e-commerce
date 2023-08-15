from django.db import models
from django.contrib.auth.models import User
from base.models import *


# Create your models here.

class customer (models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE,null = True) 
    email = models.EmailField(max_length =80, null=True)
    email_is_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=10,null=True)
    venue = models.ForeignKey(address,null= True, on_delete=models.CASCADE)
    Orders_till_now = models.ManyToManyField(orders,null=True)
    activities = models.ManyToManyField(review,null=True)
    
    

    def __str__(self) -> str:
        return self.name.username


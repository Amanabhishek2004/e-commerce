from typing import Collection, Optional
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# category
class category(models.Model):
    name = models.CharField( max_length=50)
    def __str__(self) -> str:
        return self.name

# address
class address(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(null=True, max_length=200)
    
    # list=list(self.name)
    
    def __str__(self):
        for i in range(100):
            if ',' in self.name[:i] :
                break
        return self.name[:i-1]
          

# product


class product(models.Model):
    price = models.BigIntegerField(null=True)
    name = models.CharField(null=True, max_length=50)
    type = models.ForeignKey(category,null =True,on_delete=models.CASCADE)
    for_sale =models.PositiveIntegerField(null = True)
    created_at = models.DateTimeField(default=timezone.now)  # Add the created_at field

    def __str__(self) -> str:
          return self.name

# cart


class cart(models.Model):
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField( auto_now=True, auto_now_add=False,null=True)
    item = models.ForeignKey(product, null =True , on_delete=models.CASCADE)
    created = models.DateTimeField( auto_now=True, auto_now_add=False,null =True)
    quantity = models.PositiveIntegerField(default=1)
    deliver_to = models.ForeignKey(address,null =True,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.item} Added by  {self.ordered_by}'
    # class Meta:
    #     ordering = [-'created']




# customer

class customer (models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE,null = True) 
    email = models.EmailField(max_length =80)
    venue = models.ForeignKey( address,null= True, on_delete=models.CASCADE)      

    def __str__(self) -> str:
        return 
# orders
class orders(models.Model):
    tracking_id = models.BigIntegerField(null =True)
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE,null =True)
    name = models.ForeignKey(product, null=True, on_delete=models.CASCADE)
    deliver_to = models.ForeignKey(address,null =True,on_delete=models.CASCADE)
    no_of_items = models.PositiveIntegerField(null =True,default=0)
    total_amount = models.BigIntegerField(null =True,blank=True)

class review(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    Product = models.ForeignKey(product,null=True , on_delete= models.CASCADE)

    def __str__(self):
        return f"Review of {self.Product} by {self.user}"
    
# STATUS_ORDER = (('order confirmed','order confirmed'),('order shipped','order shipped'),(''),('out for deliver','out for delivery'))
class status(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name


class order_tracking(models.Model):
    
    tracking_id = models.BigIntegerField(null =True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null =True)
    Product = models.ForeignKey(product,null=True , on_delete= models.CASCADE)
    dlivery_status = models.ManyToManyField(status,null=True,max_length=200)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
        
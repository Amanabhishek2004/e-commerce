from django import forms
from .models import *
class order_through_cart_form(forms.Form):
    
    amount = forms.IntegerField( label='quantity')
    
       
    

    

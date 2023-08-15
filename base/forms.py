from django import forms
from .models import *





class order_through_cart_form(forms.Form):
    
    amount = forms.IntegerField( label='quantity')
    Address = forms.ChoiceField(label = "Address" ) 
class review_edit_form(forms.ModelForm):
    class Meta:
        model = review
        fields = ["body"]      
    

    

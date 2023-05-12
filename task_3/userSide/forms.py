from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import CheckoutModel

# from .models import Product_List

# userside forms are here


# invoice 
class CheckoutForm ( forms.ModelForm ):
    class Meta:
        model = CheckoutModel

        fields = [ 

            "UserName",
            "ProductId",
            "ProductName",
            "Quantity",
            "CouponCode",
            "TotalPrice",
            "Sponsor" 

        ]

        
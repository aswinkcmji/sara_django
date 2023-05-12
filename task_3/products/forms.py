from django import forms
from .models import Product_List

class addStockForm( forms.ModelForm ):

  Product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border ps-2'}))
  Price = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control border ps-2','min':'1'}))
  Quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control border ps-2','min':'1'}))
  Image_Link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border ps-2'}))
  class Meta:
    model = Product_List
    fields = ('Product_name','Price','Quantity','Image_Link',)
    

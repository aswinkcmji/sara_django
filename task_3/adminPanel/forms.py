from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import GenerateCoupon, NewUserModel, BadgeDetailsModel
# creating a form
# class AdminInputForm(forms.Form):

# 	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputfield'}))
# 	password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'inputfield'}))
	
# class AddUserForm(forms.Form):

# 	firstname = forms.CharField(widget = forms.TextInput(attrs={'class': 'inputfield'}))
# 	lastname = forms.CharField(widget = forms.TextInput(attrs={'class': 'inputfield'}))
# 	username = forms.CharField(widget = forms.TextInput(attrs={'class': 'inputfield'}))
# 	dob = forms.CharField(widget = forms.DateInput(attrs={'class': 'inputfield'}))
# 	first_name = forms.CharField(widget = forms.TextInput(attrs={'class': 'inputfield'}))

class addUserForm(UserCreationForm):

	sponsor = forms.CharField(max_length=32)
	first_name = forms.CharField(max_length=32)
	last_name = forms.CharField(max_length=32)
	email = forms.EmailField(max_length=64)

	class Meta(UserCreationForm.Meta):
		model = NewUserModel
		# I've tried both of these 'fields' declaration, result is the same
		# fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
		fields = UserCreationForm.Meta.fields + ('sponsor','first_name', 'last_name', 'email',)

		# widgets = {
		# 	'username': forms.TextInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
		# 	'first_name': forms.TextInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
		# 	'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
		# 	'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
		# 	'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
		# 	'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
		# }

class  addToWallet(forms.ModelForm):

	wallet = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control border mt-4 p-2 inputfield','min':'1','placeholder':'Enter the amount'}),label='')
	class Meta:
		
		model = NewUserModel
		fields = ('wallet',)


class generateCoupon(forms.ModelForm):
	creator = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border mt-4 p-2','min':'1','readonly':'true'}),label='')
	couponid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border mt-4 p-2 ','min':'1','readonly':'true'}),label='')
	amount = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control border mt-4 p-2 inputfield','min':'1','placeholder':'Enter the amount'}),label='')
	class Meta:
		model = GenerateCoupon
		fields = ('creator','couponid','amount',)


class BadgeDetailsForm( forms.ModelForm ) :
	badgeid = forms.CharField(widget = forms.NumberInput(attrs={'hidden':'true'}))
	class Meta :
		model = BadgeDetailsModel
		
		fields = (
			'badgeid',
			'badge',
            'badgeamount',
            'sponsorbonus',
		)
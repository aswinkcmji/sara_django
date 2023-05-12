from urllib import response
from django.shortcuts import render,redirect, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from products.models import Product_List
from userSide.models import CheckoutModel

from products import views
from .forms import CheckoutForm
from django.contrib import messages

from django.contrib.auth import authenticate, login ,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control 
from adminPanel.forms import addUserForm, generateCoupon
from django.contrib import messages
from adminPanel.models import NewUserModel,GenerateCoupon,QueueModel
import json
# Create your views here.

class Home(View):

	def get(self, request, *args, **kwargs):
		product = Product_List.objects.all()
		stu = {
			"product":product
		}
		print(product.query)
		return render(request, 'index.html',stu)


class Shop(View):

	def get(self, request, *args, **kwargs):
		product = Product_List.objects.all().exclude(Quantity = 0)
		count = len(product)
		stu = {
			"product":product,
			"count":count
		}
		print(product)
		return render(request, 'shop-grid.html',stu)


@method_decorator(login_required,name='dispatch')
class Checkout(View):

	def get(self, request, id, *args, **kwargs):
		sponsor = NewUserModel.objects.filter(username = request.user).values_list('sponsor')[0][0]
		print("sponsor: %s" % sponsor)
		product =  dict( 
			list ( 
					Product_List.objects.filter(id=id).values()
				)[0]
			)

		context = { 

				'checkout_form': CheckoutForm(),
				'product' : product,
				'username' : request.user,
				'sponsor' : sponsor,
		}
		
		print( context )

		return render( request, 'checkout.html', context )


	def post(self, request, *args, **kwargs):

		checkout_modal = CheckoutForm( request.POST )
		product_object = Product_List.objects.filter( id = checkout_modal['ProductId'].value() )
		personal_object = NewUserModel.objects.filter( id = request.user.id).values('personal_sale')
		wallet_object = NewUserModel.objects.filter( id = request.user.id).values('wallet')

		

		coupon = checkout_modal['CouponCode'].value()
		
		wallet = NewUserModel.objects.filter( id = request.user.id).values_list('wallet')[0][0]
		available_coup = [ a["couponid"] for a in list(GenerateCoupon.objects.values('couponid')) ]
		
		# if form validation done then
		if checkout_modal.is_valid():

			# if coupon id not found 
			if checkout_modal["CouponCode"].value() == None :

				# if wallet has money
				if int ( checkout_modal['TotalPrice'].value() ) <= wallet :
					quantity = Product_List.objects.filter( id = checkout_modal['ProductId'].value() ).values_list("Quantity",flat=True)[0]
						
					#  ProductModal Quantity updation
					product_object.update( Quantity = int( quantity ) - int( checkout_modal['Quantity'].value() ) )

					# print( "perosna lonject : ", personal_object[0])
					personal_object.update( personal_sale = float(personal_object[0]["personal_sale"]) +  float(checkout_modal['TotalPrice'].value()) )

					personal_object.update( wallet = float(wallet_object[0]["wallet"]) -  float(checkout_modal['TotalPrice'].value()) )
					
					adminwallet = NewUserModel.objects.filter(username = 'admin').get().wallet

					NewUserModel.objects.filter(username = "admin").update( wallet = adminwallet + float(checkout_modal['TotalPrice'].value()) )					
					
					checkout_modal.save()

					messages.success(request, "Dome ! Succesfully Purchased ")

					QueueModel.objects.create(
						username=request.POST["UserName"],
						sponsor=request.POST["Sponsor"],
						totalprice=request.POST["TotalPrice"]
					)
					pass

				else :
					messages.error(request, "Ooops ! insufficiant bvalce in wallet")

			else:
				# if coupon available then ->
				if coupon in available_coup:

					couponbalance = GenerateCoupon.objects.filter(couponid = coupon).values_list('amount')[0][0]
					coupon_object = GenerateCoupon.objects.filter(couponid = coupon).values('amount')


					if couponbalance >= int( checkout_modal['TotalPrice'].value() ):						
						
						quantity = Product_List.objects.filter( id = checkout_modal['ProductId'].value() ).values_list("Quantity",flat=True)[0]
						
						#  ProductModal Quantity updation
						product_object.update( Quantity = int( quantity ) - int( checkout_modal['Quantity'].value() ) )

						#  UserModal Personal_sale updation
						personal_object.update( personal_sale = float(personal_object[0]["personal_sale"]) +  float(checkout_modal['TotalPrice'].value()) )

						checkout_modal.save()
						
						# updating coupon balance here
						coupon_object.update( amount = couponbalance - float(checkout_modal['TotalPrice'].value() ) )

						# deleting coupon if hase no money left
						if list ( GenerateCoupon.objects.filter(couponid = coupon ).values() )[0]['amount'] < 1 :
							GenerateCoupon.objects.filter(couponid = coupon ).delete()
						
						# GenerateCoupon.objects.filter(couponid = coupon).delete()

						adminwallet = NewUserModel.objects.filter(username = 'admin').get().wallet
						NewUserModel.objects.filter(username = "admin").update( wallet = adminwallet + float(checkout_modal['TotalPrice'].value()) )					
						checkout_modal.save()

						messages.success(request, "Dome ! Succesfully Purchased ")

						QueueModel.objects.create(
							username=request.POST["UserName"],
							sponsor=request.POST["Sponsor"],
							totalprice=request.POST["TotalPrice"]
						)

					else:
						messages.error(request, 'Ooops ! Insufficient balance')

				# if coupon not exist then ->
				else:
					messages.error(request, 'Ooops! No coupon found')
			
		# if form validation done then
		else : 
			messages.error(request, 'Ooops ! something went wrong. ')

		
		return redirect('checkout',id=checkout_modal['ProductId'].value() )
	

class Register(View):
	template = 'registeruser.html'
	def get(self, request, *args, **kwargs):

		form = addUserForm()
		
		context = {'form': form,
					'data': 'Add User'}
		# if request.user.is_superuser:
		# 	return render(request,self.template,context)
		# else:
		return render(request,self.template,context)
	def post(self, request, *args, **kwargs):
				if request.method == 'POST':
						form = addUserForm(request.POST)
						if form.is_valid():
							data = request.POST.get('sponsor')
							if not NewUserModel.objects.filter(username=data).exists():
								print("errroooooooorr")
								messages.error(request, 'Enter A Valid Sponsor!!!')
								return redirect('register')
							else:
								print(data)
								form.save()
								messages.success(request, 'Form submission successful')
								return redirect('register')
							#print(form.cleaned_data.get('nothing'))
				else:
					form = addUserForm()
					return render(request, self.template, {'form': form, 'title':'register here'})
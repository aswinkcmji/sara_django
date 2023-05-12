from http.client import HTTPResponse
from operator import and_
from re import M
from unittest import loader
from django.views import View
from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login ,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from userSide.models import CheckoutModel 
from .models import GenerateCoupon, NewUserModel, BadgeDetailsModel,BonusHistoryModel
from django.contrib.auth.models import User
from .forms import addToWallet,addUserForm, generateCoupon, BadgeDetailsForm
from django.contrib import messages
from django.db.models import Q
from products.models import Product_List

import random


# HOMEPAGE
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@method_decorator(login_required,name='dispatch')

class HomePage(View):

    def get(selt,request):
        
        template = 'dashboard.html'

        userCount = NewUserModel.objects.filter(~Q(username ='admin')).count()
        lastuser= NewUserModel.objects.latest('id').first_name
        stockCount = Product_List.objects.count()
        if Product_List.objects.count() >=1:
            laststock = Product_List.objects.latest('id').Product_name
        else:
            laststock = '   '
        
            
        balance = NewUserModel.objects.filter(username=request.user).values_list('wallet')[0][0]
        personal_sale = NewUserModel.objects.filter(username=request.user).values_list('personal_sale')[0][0]
        downline_saletotal = NewUserModel.objects.filter(sponsor=request.user).values_list('personal_sale')
        downline_sale_ar = []
        downline_sale = 0
        for i in downline_saletotal:
            downline_sale_ar += i
        for i in downline_sale_ar:
            downline_sale += i
        sales = CheckoutModel.objects.values_list('TotalPrice')
        totalsaledict = []
        totalsale = 0        
        for i in sales:
            totalsaledict += i
        for i in totalsaledict:
            totalsale += i


        totalbonus = NewUserModel.objects.filter(username=request.user).values_list('bonus')[0][0]

        badge = "null"
        # badge displaying
        if personal_sale >=0 and personal_sale <= 999:
            current_badge = BadgeDetailsModel.objects.filter(badgeamount=500).values_list("badge")[0][0]
            NewUserModel.objects.filter(username = request.user.username).update(badge = current_badge)
            badge = "BRONZE"    
        elif personal_sale >= 1000 and personal_sale <= 1999:
            current_badge = BadgeDetailsModel.objects.filter(badgeamount=1000).values_list("badge")[0][0]
            print("==============",type(current_badge),request.user.username,"==============")
            NewUserModel.objects.filter(username = request.user.username).update(badge = current_badge)
            badge = "SILVER"
        elif personal_sale >= 2000 and personal_sale <= 4999:
            current_badge = BadgeDetailsModel.objects.filter(badgeamount=2000).values_list("badge")[0][0]
            NewUserModel.objects.filter(username = request.user.username).update(badge = current_badge)
            badge = "GOLD"
        elif personal_sale >= 5000 and personal_sale <= 9999:
            current_badge = BadgeDetailsModel.objects.filter(badgeamount=5000).values_list("badge")[0][0]
            NewUserModel.objects.filter(username = request.user.username).update(badge = current_badge)
            badge = "PLATINUM"
        elif personal_sale >= 10000 :
            current_badge = BadgeDetailsModel.objects.filter(badgeamount=10000).values_list("badge")[0][0]
            NewUserModel.objects.filter(username = request.user.username).update(badge = current_badge)
            badge = "DIAMOND"


        context = {
                'my': "",
                'count': userCount,
                'lastuser': lastuser,
                'stockcount': stockCount,
                'laststock': laststock,
                'balance': balance,
                'personal_sale': personal_sale,
                'downline_sale': downline_sale,
                'totalsale': totalsale,
                'badge' : badge,
                'totalbonus':totalbonus,
                    # 'lastsale': last_sale,

                
            }
        return render(request,template,context)

        
# # LOGINPAGE

# class LoginPage(LoginView):

#     template_name = 'login.html'

#     def get(self, request, *args, **kwargs):
#         context ={}
#         context['form'] = addUsers()
#         return render(request,self.template_name, context)
#     def post(self, request, *args, **kwargs):
#         print(request.POST['username'])
#         print(request.POST['password'])
#         user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
#         is_active = NewUserModel.objects.get(username=request.POST['username'])
#         if is_active:
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#         else:
#             messages.success(request, 'Faild to login')
#             return HttpResponseRedirect(reverse('login'))
    

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


# table
@method_decorator(login_required,name='dispatch')

class Table(View):
    def get(self, request, *args, **kwargs):
        userData = NewUserModel.objects.filter(~Q(username ='admin')).order_by('first_name').values()
        # print(userData,"1111111111111111111111111111")
        blockedUser = NewUserModel.objects.filter(is_active = False).order_by('first_name').values()
        purchase_history = CheckoutModel.objects.all().values()
        purchase_history_user = CheckoutModel.objects.filter(UserName = request.user).values()
        downline_purchase = CheckoutModel.objects.filter(Sponsor = request.user).values()
    


        template = 'tables.html'
        context = {
                'data': "Table",
                'userData': userData,
                'blockedUser':blockedUser,
                'purchase': purchase_history,
                'purchase_history_user': purchase_history_user,
                'purchase_user': downline_purchase,
            }
            
        return render(request,template,context)


# billing
@method_decorator(login_required,name='dispatch')

class Billing(View):
    def get(self, request, *args, **kwargs):
        form1 = addToWallet()
        form2 = generateCoupon()
        # getlastid = GenerateCoupon.objects.latest('id').couponid
        getcoupon = GenerateCoupon.objects.all().values()
        getcouponuser = GenerateCoupon.objects.filter(creator = request.user)

        # list of available coupon codes 
        couponids = [ couponcode for couponcode in list ( GenerateCoupon.objects.values_list('couponid', flat=True ) ) ]

        # calling coupon manager
        self.couponmanager( couponids )
 
        #couopn code generaton 
        def coupongenerator ( coupons, code = ''.join( [ random.choice( 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' ) for _ in  range(6) ] ).strip() ) -> str :
            if code in coupons :
                return coupongenerator( coupons )
            
            return code 
                
        template = 'billing.html'
        context = {
            'data': "Coupon", 
            'form1': form1,
            'form2': form2,
            'user':request.user.username,
            'id': coupongenerator( couponids ),
            'coupon':getcoupon,
        }
                
        print("helo from : ", context['user'])
        return render(request, template, context)


    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            walletamount = NewUserModel.objects.filter(username=user).values_list('wallet')[0][0]
            NewUserModel.objects.filter(username=user).update(wallet= int(request.POST.get('wallet'))+int(walletamount))
            return redirect('billing')
            
        except Exception:
            couponForm = generateCoupon(request.POST)
            if couponForm.is_valid():
                walletamount = NewUserModel.objects.filter(username=user).values_list('wallet')[0][0]
                print("wallet amount                     : ",walletamount)
                couponamount = int(request.POST.get('amount'))
                if walletamount >= couponamount:
                    NewUserModel.objects.filter(username=request.user).update(wallet= int(walletamount)-int(request.POST.get('amount')))
                    print("useeeeeeeeeeeeeeeeeeeeeeeeeeeeer",request.user)                 
                    couponForm.save()
                    messages.success(request, 'Form submission successful')
                    return redirect('billing')
                else:
                    messages.success(request, 'Insufficient Wallet Balance.')
                    return redirect('billing')    
            else:
                couponForm = addUserForm()
                return redirect('billing')
        
    # manage coupons
    def couponmanager (self, couponids ) :
        for ids in couponids :
            if list ( GenerateCoupon.objects.filter(couponid = ids ).values() )[0]['amount'] < 1 :
                GenerateCoupon.objects.filter(couponid = ids ).delete()


# Notifications
@method_decorator(login_required,name='dispatch')

class History(View):
    def get(self, request, *args, **kwargs):
        history = BonusHistoryModel.objects.filter(sponsor = request.user.username)
        adminhistory = BonusHistoryModel.objects.all()

        template = 'notifications.html'
        context = {
                'data': history,
                'admindata' :adminhistory,
            }
        return render(request,template,context)

# addUserForm
@method_decorator(login_required,name='dispatch')

class AddUser(View):
    template = 'user/adduser.html'
    def get(self, request, *args, **kwargs):

        form = addUserForm()
        user = request.user
        
        context = {'form': form,
                    'data': 'Add User',
                    'user': user,
                    }
        
        return render(request,self.template,context)
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
                form = addUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Form submission successful')
                    return redirect('adduser')
                else:
                    messages.warning(request, 'Form submission failed')
                    return redirect('adduser')
                    # print(form.cleaned_data.get('nothing'))
        else:   
            form = addUserForm()
            return render(request, self.template, {'form': form, 'title':'register here'})

# UserTable
@method_decorator(login_required,name='dispatch')
class UserTable(View):
    template = 'user/usertable.html'
    def get(self, request, *args, **kwargs):

        userData = NewUserModel.objects.filter(~Q(username ='admin')).order_by('first_name').values()
        # print(userData,"88888888888888888888888888888888")
        i = 0
        context = { 'userData':userData,
                    'data': 'User Table',
                    'id':i}
        if request.user.is_superuser:
            return render(request,self.template,context)
        else:
            return render(request,'403error.html',context)
    # def post(self, request, *args, **kwargs):
    #     print()

class UpdateUser(View):
    def get(self , request, id,*args, **kwargs):
        user = NewUserModel.objects.get(id=id)
        print(user.is_active)
        if user.is_active:
            user.is_active = False 
            user.save()
        else:
            user.is_active = True
            user.save()
            
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('usertable'))   
        else:
            return render(request,'403error.html',{})



class Bonuslist( View ):
    template ='bonuslist.html'
    def get(self, request, *args, **kwargs):
        bonus = BadgeDetailsModel.objects.values()
        print(bonus,"-------gggggggggggggggggggg")

        if request.user.is_superuser:
            return render( request,self.template, { "table" : bonus,'badgeconfig_form' : BadgeDetailsForm(),})
        else:
            return render(request,'403error.html',{})
        

    def post(self, request, *args, **kwargs):

        badgedetail_form = BadgeDetailsForm( request.POST )
        
        badgedetail_object = BadgeDetailsModel.objects.filter( id = badgedetail_form["badgeid"].value() )

        badgedetail_object.update( 
            badgeamount = badgedetail_form["badgeamount"].value(),
            sponsorbonus = badgedetail_form["sponsorbonus"].value()
        )

            # sponsorbonus = badgedetail_form["sponsorbonus"].value(),

        print(badgedetail_form["sponsorbonus"].value())


        return redirect('bonustable' )
        
    
# class EditBonus(View):
#     def get(self , request, id,*args, **kwargs):
#         item = BadgeDetailsModel.objects.get(id=id)
#         print(item,"going to eeeeeeeeeeeeeeeeeeeeeedddiiiiiiiiiiiiiiiiiiittt")
#         # item.delete()
#         # return HttpResponseRedirect(reverse('bonustable'))
#         return render( request,'editbonus.html', {})
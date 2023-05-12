from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

class addUsers(models.Model):
    
    first_name = models.TextField(max_length=50, blank=False)
    last_name = models.TextField(max_length=50, blank=True)
    username = models.TextField(max_length=25, blank=False,unique=True)
    email = models.EmailField(max_length=50, blank=False)

    password = models.TextField(max_length=15, blank=False)


class NewUserModel(AbstractUser):
    
    sponsor = models.CharField(max_length=32,null=True)
    personal_sale = models.FloatField(max_length=100,null=False,default=0)
    wallet = models.FloatField(null=False,default=0)
    badge = models.IntegerField(null=False,default=0)
    bonus = models.FloatField(null=False,default=0)

class GenerateCoupon(models.Model):
    
    creator = models.TextField(max_length=50, blank=False)
    couponid = models.TextField(max_length=50, blank=False,unique=True)
    amount = models.FloatField( blank=False)

class BadgeDetailsModel(models.Model):
    
    badge = models.IntegerField(blank=False)
    badgeamount = models.FloatField(blank=False)
    sponsorbonus = models.FloatField( blank=False)

class QueueModel(models.Model):
    username = models.CharField(max_length=32 , blank=False)
    sponsor = models.CharField(max_length=32, blank=False)
    totalprice = models.FloatField(null=False, blank=False)

class BonusHistoryModel(models.Model):
    username = models.CharField(max_length=32, blank=False)
    sponsor = models.CharField(max_length=32, blank=False)
    bonusamount = models.FloatField(null=False, blank=False)
    purchasedamount = models.FloatField(null=False, blank=False)

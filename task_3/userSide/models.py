from django.db import models
from django.conf import settings
    
# Create your models here.
class CheckoutModel(models.Model):

    UserName = models.CharField(max_length = 32, blank = False, )
    ProductId = models.CharField( max_length = 16, blank = False, )
    ProductName = models.CharField( max_length = 32, blank = False, )
    Quantity = models.IntegerField(blank = False, )
    CouponCode = models.CharField( max_length = 62, blank = True, )
    TotalPrice = models.FloatField( max_length = 32, blank = False )
    Sponsor = models.CharField(max_length = 32, blank = False, )
    
    pass
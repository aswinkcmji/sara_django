from django.db import models

# Create your models here.
class Product_List(models.Model):
    Product_name = models.TextField(max_length=100, blank=False)
    Price = models.FloatField(max_length=20, blank=False)
    Quantity = models.IntegerField(blank=False,)
    Image_Link = models.TextField(max_length=100, blank=False)
    
    def __str__(self):
        return str(self.id)

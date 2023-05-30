from django.db import models
from accounts.models import User
from userHomePage.models import Order
# Create your models here.

class CouponCode(models.Model):
    code = models.CharField(max_length=255)
    discount = models.IntegerField()
    percentage_or_not = models.BooleanField(default=False)
    cart_value = models.IntegerField(default=0)

class AffiliateCommission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  
    commission_title = models.CharField(max_length=255,null=True,blank=True)
    commission = models.IntegerField(default=0) 
    status = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
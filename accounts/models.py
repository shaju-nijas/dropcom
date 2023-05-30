from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Users(models.Model):
    user = models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    referral_id = models.CharField(max_length=200)
    invited_by_id = models.CharField(default=0,max_length=200,null=True,blank=True)
    invited_user = models.CharField(max_length=255,null=True,blank=True)
    wallet = models.IntegerField(default=0)
    total_earnings = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    date_time_of_joining = models.DateTimeField(auto_now_add=True)
    refunded_amount = models.IntegerField(default=0,null=0,blank=0)

    level_1_count = models.IntegerField(default=0)
    level_2_count = models.IntegerField(default=0)
    level_3_count = models.IntegerField(default=0)
    level_4_count = models.IntegerField(default=0)
    level_5_count = models.IntegerField(default=0)
    level_6_count = models.IntegerField(default=0)
    level_7_count = models.IntegerField(default=0)
    
    level_1_earnings = models.IntegerField(default=0)
    level_2_earnings = models.IntegerField(default=0)
    level_3_earnings = models.IntegerField(default=0)
    level_4_earnings = models.IntegerField(default=0)
    level_5_earnings = models.IntegerField(default=0)
    level_6_earnings = models.IntegerField(default=0)
    level_7_earnings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username } | {self.user.email}"

class Subscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_time_of_payment = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField()
    razorpay_order_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return f"{self.user.username } | {self.payment_status} | {self.date_time_of_payment}"

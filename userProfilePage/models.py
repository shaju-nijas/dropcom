from django.db import models
from accounts.models import User
# Create your models here.

class Withdraws(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    withdraw_requested_amount = models.CharField(max_length=100)
    withdraw_requested = models.BooleanField(default=False)
    withdraw_completed = models.BooleanField(default=False)
    withdraw_status = models.BooleanField(default=False)
    withdrawed_amount = models.CharField(max_length=100,null=True,blank=True)
    date_time_of_withdraw_requested = models.DateTimeField()
    date_time_of_withdraw_completed = models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return self.user.username

class ContactUs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField(null=True,blank=True)
    seen = models.BooleanField(default=False)
 
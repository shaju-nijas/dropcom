from django.db import models
from accounts.models import User
# Create your models here.

class Lottodrop(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    number = models.CharField(max_length=100)
    result_number = models.CharField(max_length=100,blank=True,null=True)
    Result = models.BooleanField(default=False) 
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(CarouselImages)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)
admin.site.register(BankAccountDetails)
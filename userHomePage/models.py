from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categories(models.Model):
    category = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='categories')
    def __str__(self) -> str:
        return self.category

class Products(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255)
    name = models.CharField(max_length=255) 
    brand = models.CharField(max_length=255,null=True,blank=True)   
    mrp = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    description = models.TextField()
    image = models.ImageField(upload_to='products')    
    def __str__(self) -> str:
        return f"{self.category} | {self.name}"
    
class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)  
    quantity = models.IntegerField(default=1)

    def __str__(self) :
        return f"{self.quantity} of {self.product.name}" 

    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_total_list_price(self):
        return self.quantity * self.product.mrp

    def get_final_price(self):
        return self.get_total_item_price()  

    def get_final_list_price(self):
        return self.get_total_list_price()        

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True,blank=True)
    coin_discount = models.FloatField(default=0.0,null=True,blank=True)
    coupon_discount = models.FloatField(default=0.0,null=True,blank=True)
    ordered = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100,unique=True,default=None,blank=True,null=True)
    
    date_time_of_Payment = models.DateTimeField(null=True,blank=True)
    order_recieved = models.BooleanField(default=False)
    order_shipped = models.BooleanField(default=False)
    order_delivered = models.BooleanField(default=False)
    order_expected_delivery_date = models.DateTimeField(max_length=200,null=True,blank=True)
    order_cancelled = models.BooleanField(default=False)
    tracking_id_title = models.CharField(max_length=255,null=True,blank=True)
    tracking_id = models.CharField(max_length=255,null=True,blank=True)
    order_cancelled_by_admin = models.BooleanField(default=False)
    order_return_requested = models.BooleanField(default=False)
    order_returned = models.BooleanField(default=False)
    returned_order_refund_requested = models.BooleanField(default=False)
    returned_order_refunded = models.BooleanField(default=False)

    razorpay_order_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank=True)

    def save(self,*args,**kwargs):
        if self.order_id is None and self.date_time_of_Payment and self.id:
            self.order_id = self.date_time_of_Payment.strftime('ORDERID%y%m%dODR')+str(self.id)
        return super().save(*args,**kwargs)

    def __str__(self) :
        return self.user.username 

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price() 
        return total
    
    def get_total_final_price(self):
        return self.get_total_price() - self.coin_discount - self.coupon_discount 
    
    def get_total_list_price(self):
        total_list_price = 0
        for order_item in self.items.all():
            total_list_price += order_item.get_final_list_price()  
        return total_list_price

    def get_total_count(self):
        order = Order.objects.get(id = self.id)
        return order.items.count()        

class CheckoutAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=100)

    def __str__(self) :
        return self.user.username    
    
class CarouselImages(models.Model):
    image = models.ImageField(upload_to='carousel')

class BankAccountDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    IFSC_code = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    bank_branch = models.CharField(max_length=255)
    withdraw_requested = models.BooleanField(default=False)

class ReturnOrdersRefund(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    return_Date = models.DateTimeField(null=True,blank=True)
    return_Amount = models.CharField(max_length=255, null=True,blank=True)
    returned_Order = models.ForeignKey(Order,on_delete=models.CASCADE)
    return_requested = models.BooleanField(default=False)
    return_success = models.BooleanField(default=False)  
    return_amount_paid = models.BooleanField(default=False)

class ReturnOrdersBankDetails(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    acc_holder_name = models.CharField(max_length=255)
    acc_num = models.CharField(max_length=255)
    IFSC_code = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    bank_branch = models.CharField(max_length=255)
    withdraw_requested = models.BooleanField(default=False)
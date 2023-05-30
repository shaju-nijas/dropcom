from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from userHomePage.models import OrderItem,CheckoutAddress,Order,Products
from accounts.models import Users,Subscription
from products.models import CouponCode,AffiliateCommission
from django.urls import reverse
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_SECRET))
# Create your views here.

def add_delivery_address(request):
    if request.user.is_authenticated:
        subscribe = Subscription.objects.get(user = request.user)
        if subscribe.payment_status == True:
            user = Users.objects.get(user=request.user,is_active = True)
            order_db = Order.objects.get(user=request.user,ordered = False) 
            if int(order_db.get_total_final_price()) > 0:
                if CheckoutAddress.objects.filter(user=request.user).exists():
                    return redirect('checkout')
                if request.method == "POST":
                    name = request.POST.get('name')
                    phone_no = request.POST.get('phone_no')
                    address = request.POST.get('address')
                    state = request.POST.get('state')
                    city = request.POST.get('city')
                    pin_code = request.POST.get('pin_code')
                    checkout_address = CheckoutAddress(
                        user = request.user,
                        name = name,
                        phone_no = phone_no,
                        address = address,
                        state = state,
                        city = city,
                        pin_code = pin_code,
                    )
                    checkout_address.save()
                    return redirect('checkout')
                return render(request,'products-page/checkout-address.html') 
            else:
                print('you cheat')
                return HttpResponse('404 error occured') 
        else:
            return redirect('/accounts/buy-subscription')
    return redirect('/accounts')
    
def edit_delivery_address(request):
    if request.method == "POST":
        name = request.POST['name']
        phone_no = request.POST['phone_no']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        pin_code = request.POST['pin_code']
        CheckoutAddress.objects.filter(user = request.user).update(
            name = name,
            phone_no = phone_no,
            address = address,
            state = state,
            city = city,
            pin_code = pin_code,
        )
        return redirect(checkout)
    return render(request,'products-page/edit-checkout-address.html')

def cart(request):
    if request.user.is_authenticated:
        subscribe = Subscription.objects.get(user = request.user)
        if subscribe.payment_status == True:
            user = Users.objects.get(user=request.user,is_active = True)
            if Order.objects.filter(user = request.user,ordered = False).exists():
                order  = Order.objects.get(user = request.user,ordered = False)
                if int(order.get_total_final_price()) <= 0:
                    order.coupon_discount = 0
                    if order.coin_discount != 0:
                        user.coins = int(order.coin_discount)
                        user.save()
                        order.coin_discount = 0
                        order.save()
                    else:
                        order.save()    
                return render(request,'products-page/cart.html',{'order':order,'user':user})
            return render(request,'products-page/cart.html',{'user':user}) 
        else:
            return redirect('/accounts/buy-subscription')
    return redirect('/accounts')  

def add_to_cart(request,id):
    if request.user.is_authenticated:
        subscribe = Subscription.objects.get(user = request.user)
        if subscribe.payment_status == True:
            user = Users.objects.get(user=request.user,is_active = True)  

            product = Products.objects.get(id=id)

            order_item,created = OrderItem.objects.get_or_create(
                product = product,
                user = request.user,
                quantity = 1,
                ordered = False,
            )
            order_qs = Order.objects.filter(user = request.user,ordered = False)
            if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(product__id = id).exists():
                    order_item.quantity +=1
                    order_item.save()
                    print("added item quantity")
                    return redirect('cart')
                else:
                    order.items.add(order_item)
                    print("item added to cart") 
                    return redirect('cart')
            else:
                order = Order.objects.create(user = request.user)
                order.items.add(order_item)
                print("item added to cart")
                return redirect('cart')  
        else:
            return redirect('/accounts/buy-subscription')
    return redirect('/accounts')  

def delete_cart(request,id):
    product = Products.objects.get(id=id)
    order_item = OrderItem.objects.filter(
        product = product,
        user = request.user,
        ordered = False,
    )
    order_item.delete()
    messages.error(request,'Item deleted..!!')
    return redirect('cart')


def apply_coin(request):
    get_user = Users.objects.get(user = request.user)
    if get_user.coins > 0:
        order_db = Order.objects.get(user = request.user,ordered = False)
        order_db.coin_discount = get_user.coins
        order_db.save()
        get_user.coins = 0
        get_user.save() 
        print('coins applied')
        messages.success(request,'Coins appiled successfully')
        return redirect('cart') 
    else:
        messages.error(request,'No coins applied..!!')
        return redirect('cart')
    
def apply_coupon(request):
    if request.method == "POST" :
        code = request.POST['code']

        if CouponCode.objects.filter(code = code).exists():
            get_coupon = CouponCode.objects.get(code = code)
            order_db = Order.objects.get(user=request.user,ordered = False)
            total_amount = int(order_db.get_total_price())
            if total_amount >= get_coupon.cart_value:
                if get_coupon.percentage_or_not == True :
                    discount = (get_coupon.discount / 100)*int(order_db.get_total_price())
                    order_db.coupon_discount = int(discount)
                    order_db.save()
                    messages.success(request,"Coupon applied successfully")  
                    return redirect('cart')
                else:
                    order_db.coupon_discount = get_coupon.discount
                    order_db.save()
                    messages.success(request,"Coupon applied successfully")  
                    return redirect('cart')
            else:
                balance = get_coupon.cart_value - total_amount
                messages.error(request,"need ",balance," rs products in your cart to apply coupon")  
                return redirect('cart')
        else:
            messages.error(request,"Enter valid coupon code..!")  
            return redirect('cart')        
              

def checkout(request):
    if request.user.is_authenticated:
        subscribe = Subscription.objects.get(user = request.user)
        if subscribe.payment_status == True:
            user = Users.objects.get(user=request.user,is_active = True)
            try:
                order = Order.objects.get(user = request.user,ordered = False)
                saved_price = int(order.get_total_list_price()) - int(order.get_total_final_price())
                address = CheckoutAddress.objects.get(user = request.user)
                order_amount = order.get_total_final_price()
                order_currency = "INR"
                order_reciept = order.order_id
                notes = {
                    'name':address.name,
                    'phone_no':address.phone_no,
                    'address':address.address,
                    'state':address.state,
                    'city':address.city,
                    'pin_code':address.pin_code,
                }
                razorpay_order = razorpay_client.order.create(
                    dict(
                        amount = order_amount*100,
                        currency = order_currency,
                        receipt = order_reciept,
                        notes = notes,
                        payment_capture = "0",
                    )
                )
                order.razorpay_order_id = razorpay_order["id"]
                order.save()
                return render(request,"products-page/checkout-page.html",{
                    'user':user,
                    'order' : order,
                    'order_id' : razorpay_order["id"],
                    'orderId' : order.order_id,
                    'final_price' : order_amount,
                    'razorpay_merchant_id' : settings.RAZORPAY_ID,
                    'callback_url' : "http://"+"127.0.0.1:8000"+"/products/handlerequest",
                    'address':address,
                    'saved_price':saved_price,
                })
            except Order.DoesNotExist:
                print("Order not found")
                return HttpResponse("404 Error") 
        else:
            return redirect('/accounts/buy-subscription')
    return redirect('/accounts')

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get("razorpay_payment_id","")
            order_id = request.POST.get("razorpay_order_id","")
            signature = request.POST.get("razorpay_signature","")

            para_dict = {
                "razorpay_payment_id":payment_id,
                "razorpay_order_id":order_id,
                "razorpay_signature":signature,
            }
            try:
                order_db = Order.objects.get(razorpay_order_id = order_id)
                print('order found')
            except:
                print('order not found')
                return HttpResponse("505 error occured")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()        

            result = razorpay_client.utility.verify_payment_signature(para_dict)
            
            if result is not None:

                amount = order_db.get_total_final_price()
                amount = amount * 100
                payment_status = razorpay_client.payment.capture(payment_id,amount)
                if payment_status is not None:
                    order_db.ordered = True
                    order_db.items.ordered = True
                    order_db.ordered_date = timezone.now()
                    order_db.date_time_of_Payment = timezone.now()
                    order_db.save()
                    return redirect(orderConfirmed)
                else:
                    order_db.ordered = False
                    order_db.save()
                    return HttpResponse('Payment Failed .. Try again')
            else:
                order_db.ordered = False
                order_db.save()
                return HttpResponse('Payment failed.. Try again')
        except:
            return HttpResponse("Error occured") 
        
def orderConfirmed(request):
    user = Users.objects.get(user=request.user)
    return render(request,'products-page/order-confirmed.html',{'user':user})        
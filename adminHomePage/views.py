from django.http import HttpResponse
from django.shortcuts import render,redirect
from accounts.models import Users,User
from django.contrib import messages
from datetime import datetime
from userProfilePage.models import Withdraws,ContactUs
from userHomePage.models import BankAccountDetails
from userHomePage.views import index
from userHomePage.models import Order,CheckoutAddress,ReturnOrdersBankDetails,ReturnOrdersRefund
from products.models import AffiliateCommission
from PlayAndWin.models import Lottodrop

# Create your views here.

def adminDashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'admin-page/dashboard.html')
        else:
            return redirect(index)
    else:
        return redirect('../')

def totalUsers(request):
    if request.user.is_superuser:
        active_users = Users.objects.filter(is_active = True).order_by('-id')
        inactive_users = Users.objects.filter(is_active = False).order_by('-id')
        context = {
            'active':active_users,
            'inactive':inactive_users
        }   
        return render(request,'admin-page/users.html',context)
    else:
        return redirect('../')

def withdrawReq(request):
    if request.user.is_superuser:
        withdraw = Withdraws.objects.filter(withdraw_requested = True)
        bank =  BankAccountDetails.objects.filter(withdraw_requested = True)
        users = Users.objects.filter(user__in=[withdraw.user for withdraw in withdraw])
        zip_datas = zip(withdraw , bank , users)
        context = {
            'datas':zip_datas
        }
        return render(request,'admin-page/withdraw-req.html',context)
    else:
        return redirect('../')

def withdrawCompleted(request):
    if request.user.is_superuser:
        withdraw_db = Withdraws.objects.filter(withdraw_status = True).order_by('-date_time_of_withdraw_completed')
        return render(request,'admin-page/withdraw-completed.html',{'withdraw_db':withdraw_db})
    else:
        return redirect('../')
    
def orders(request):
    if request.user.is_superuser:
        get_orders = Order.objects.filter(ordered = True,order_recieved = False,order_shipped = False,order_delivered = False,order_cancelled = False)
        return render(request,'admin-page/orders.html',{'orders':get_orders})
    else:
        return redirect('../')
    
def orderRecieved(request):
    if request.user.is_superuser:
        order = Order.objects.filter(ordered = True,order_recieved = True,order_shipped = False,order_delivered = False,order_cancelled = False)
        address = CheckoutAddress.objects.filter(user__in=order.values('user'))
        zip_data = zip(order,address)
        return render(request,'admin-page/order-recieved.html',{'datas':zip_data})
    else:
        return redirect('../')

def ordersShipped(request):
    if request.user.is_superuser:
        get_orders = Order.objects.filter(ordered = True,order_recieved = True,order_shipped = True,order_delivered = False,order_cancelled = False)
        return render(request,'admin-page/order-shipped.html',{'orders':get_orders})
    else:
        return redirect('../')

def orderDelivered(request):
    if request.user.is_superuser:
        get_orders = Order.objects.filter(ordered = True,order_recieved = True,order_shipped = True,order_delivered = True,order_cancelled = False,order_cancelled_by_admin = False,order_returned = False)
        return render(request,'admin-page/order-delivered.html',{'orders':get_orders})
    else:
        return redirect('../')

def deleteUser(request,id):
    if request.user.is_superuser:
        get_user = User.objects.filter(id = id).get()
        get_user.delete()
        messages.success(request,"user deleted successfully")
        return redirect(totalUsers)
    else:
        return redirect('../')
    
def withdrawelPayedByAdmin(request,id):
    get_user = Withdraws.objects.get(user = id ,withdraw_requested = True)
    get_user_bank = BankAccountDetails.objects.get(user = get_user.user.id, withdraw_requested = True)
    get_user.withdraw_completed = True
    get_user.withdraw_status = True
    get_user.withdraw_requested = False
    get_user.withdrawed_amount = get_user.withdraw_requested_amount
    get_user.date_time_of_withdraw_completed = datetime.now()
    get_user.save()
    get_user_bank.withdraw_requested = False
    get_user_bank.save()
    messages.success(request,"successfully payed....")
    return redirect(withdrawReq)

def recieveOrder(request,id):
    get_order = Order.objects.get(id = id)
    get_order.order_recieved = True
    get_order.save()
    messages.success(request,'order recieved successfully..')
    get_user = Users.objects.get(user = get_order.user)
    if Users.objects.filter(referral_id = get_user.invited_by_id).exists():
        invited_user = Users.objects.get(referral_id = get_user.invited_by_id)
        commission = AffiliateCommission.objects.create(
            user = invited_user.user,
            commission_title = "Commission received when your friend bought a product",
            commission = (5 / 100)*int(get_order.get_total_final_price()),
        )
    return redirect(orders)

def orderShipped(request,id):
    get_order = Order.objects.get(id = id)
    if request.method == "POST":
        tracking_id_title = request.POST['tracking_id_title']
        tracking_id = request.POST['tracking_id']
        order_expected_delivery_date = request.POST['order_expected_delivery_date']
        get_order.tracking_id_title = tracking_id_title
        get_order.tracking_id = tracking_id
        get_order.order_expected_delivery_date = order_expected_delivery_date
        get_order.order_shipped = True
        get_order.save()
        messages.success(request,'order shipped successfully')
        return redirect(orderRecieved)
    
def deliveryCompleted(request,id):
    get_order = Order.objects.get(id=id)
    get_order.order_delivered = True
    get_order.save()
    messages.success(request,"delivery completed")
    get_user = Users.objects.get(user = get_order.user)
    if Users.objects.filter(referral_id = get_user.invited_by_id).exists():
        invited_user = Users.objects.get(referral_id = get_user.invited_by_id)
        commission = AffiliateCommission.objects.get(user = invited_user.user)
        commission.status = True
        commission.save()
        invited_user.coins += commission.commission
        invited_user.save()
    return redirect(ordersShipped) 

def cancelOrderByAdmin(request,id):
    get_order = Order.objects.get(id=id)
    get_order.order_cancelled_by_admin = True
    get_order.order_cancelled = True
    get_order.save()
    messages.success(request,'order deleted successfully..')
    return redirect(orders)

def cancelledOrders(request):
    if request.user.is_superuser:
        get_orders = Order.objects.filter(order_cancelled = True)
        return render(request,'admin-page/cancelled-orders.html',{'orders':get_orders})
    else:
        return redirect('../')
    
def enquiry(request):
    datas = ContactUs.objects.all().order_by('-date')
    return render(request,'admin-page/enquiry.html',{'datas':datas})    

def enquiryReplySent(request,id):
    get_item = ContactUs.objects.get(id = id)
    get_item.seen = True
    get_item.save()
    messages.success(request,"reply sented successfully..!!")
    return redirect(enquiry)

def adminlottodrop(request):
    get_datas = Lottodrop.objects.filter(Result = False)
    return render(request,'admin-page/lottodrop.html',{'datas':get_datas})

def lottodropSubmit(request,id):
    get_lotto = Lottodrop.objects.get(id=id)
    if request.method == "POST":
        result = request.POST['lottodropResult']
        get_lotto.result_number = result
        get_lotto.Result = True
        get_lotto.save()
        messages.success(request,"success...")
        return redirect(adminlottodrop)
    else:
        messages.error(request,"error occured...!!!")
        return redirect(adminlottodrop)

def returnRequest(request):
    get_datas = ReturnOrdersRefund.objects.filter(return_requested = True,return_success = False)
    return render(request,'admin-page/return-req.html',{'datas':get_datas})

def returnProductRecieved(request,id):
    get_data = ReturnOrdersRefund.objects.get(id=id)
    get_order = Order.objects.get(order_id = get_data.returned_Order.order_id)
    get_data.return_success = True
    get_order.order_returned = True
    get_data.save()
    get_order.save()
    messages.success(request,"Order ID : "+get_data.returned_Order.order_id+" will recieved succesfully..")
    return redirect(returnRequest)

def returnRefundRequest(request):
    order = Order.objects.filter(order_returned = True,returned_order_refund_requested = True,returned_order_refunded = False)
    bank =  ReturnOrdersBankDetails.objects.filter(withdraw_requested = True)
    users = Users.objects.filter(user__in=[order.user for order in order])
    zip_datas = zip(order , bank , users)
    context = {
        'datas':zip_datas
    }
    return render(request,'admin-page/return-refund.html',context)

def refund_payed(request,id):
    get_order_db = Order.objects.get(id=id,returned_order_refund_requested = True,returned_order_refunded = False)
    get_bank_db = ReturnOrdersBankDetails.objects.get(user = get_order_db.user, withdraw_requested = True)
    get_return_db = ReturnOrdersRefund.objects.get(user = get_order_db.user, return_amount_paid=False ,returned_Order = get_order_db.id)
    get_return_db.return_requested = False
    get_return_db.return_amount_paid = True
    get_bank_db.withdraw_requested = False
    get_order_db.returned_order_refunded = True
    get_order_db.save()
    get_bank_db.save()
    get_return_db.save()
    messages.success(request,"return successfully completed of order id : "+ get_order_db.order_id)
    return redirect(returnRefundRequest)

def returnCompleted(request):
    get_datas = Order.objects.filter(order_returned = True,returned_order_refunded = True)
    return render(request,'admin-page/return-completed.html',{'datas':get_datas})
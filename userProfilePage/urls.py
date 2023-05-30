from django.urls import path,include
from userProfilePage import views

urlpatterns = [
    path('',views.profile, name='profile'),
    path('my-orders',views.userOrders, name='user_orders'),
    path('my-order-detail/<int:id>',views.userOrderDetail, name='userOrderDetail'),
    path('cancel-order/<int:id>',views.cancelOrder, name='cancel-order'),
    path('refer-earn',views.referAndEarn, name='referAndEarn'),
    path('my-coins',views.userCoins,name="userCoins"),
    path('transfer-Coins',views.transferCoins,name="transferCoins"),
    path('my-wallet',views.userWallet,name="userWallet"),
    path('add-bank-account',views.addBankAcc,name="addBankAcc"),
    path('edit-bank-account',views.editBankAcc,name="editBankAcc"),
    path('withdrawRequest',views.withdrawRequest,name="withdrawRequest"),
    path('play-and-earn-rewards/',include('PlayAndWin.urls')),
    path('contact-us',views.contactAdmin,name="contactUs"),
    path('change_passsword/<int:user_id>',views.change_passsword,name="change_passsword"),
    path('about-us',views.about_us,name="about_us"),
    path('return-order-request/<int:id>',views.returnOrderRequest,name="returnOrderRequest"),
    path('returnBankDetails/<int:id>',views.returnBankDetails,name="returnBankDetails"),
    
]

from django.urls import path
from adminHomePage import views

urlpatterns = [
    path('',views.adminDashboard,name='adminDashboard'),
    path('withdraw-requests',views.withdrawReq,name='withdrawReq'),
    path('withdraw-completed',views.withdrawCompleted,name='withdrawCompleted'),
    path('orders',views.orders,name='orders'),
    path('orders-recieved',views.orderRecieved,name='orderRecieved'),
    path('orders-shipped',views.ordersShipped,name='ordersShipped'),
    path('orders-delivered',views.orderDelivered,name='orderDelivered'),
    path('cancelledOrders',views.cancelledOrders,name='cancelledOrders'),
    path('total-users-list',views.totalUsers,name='totalUsers'),
    path('delete-user/<int:id>',views.deleteUser,name='deleteUser'),
    path('withdrawelPayedByAdmin/<int:id>',views.withdrawelPayedByAdmin,name='withdrawelPayedByAdmin'),
    path('recieveOrder/<int:id>',views.recieveOrder,name='recieveOrder'),
    path('orderShipped/<int:id>',views.orderShipped,name='orderShipped'),
    path('deliveryCompleted/<int:id>',views.deliveryCompleted,name='deliveryCompleted'),
    path('cancelOrderByAdmin/<int:id>',views.cancelOrderByAdmin,name='cancelOrderByAdmin'),
    path('enquiry',views.enquiry,name='enquiry'),
    path('enquiryReplySent/<int:id>',views.enquiryReplySent,name='enquiryReplySent'),
    path('adminlottodrop',views.adminlottodrop,name='adminlottodrop'),
    path('lottodropSubmit/<int:id>',views.lottodropSubmit,name='lottodropSubmit'),
    path('return-requests',views.returnRequest,name='returnRequest'),
    path('returnRecieved/<int:id>',views.returnProductRecieved,name='returnProductRecieved'),
    path('return-Refund-Request',views.returnRefundRequest,name='returnRefundRequest'),
    path('refund_payed/<int:id>',views.refund_payed,name='refund_payed'),
    path('returnCompleted',views.returnCompleted,name='returnCompleted'),
]
from django.urls import path
from products import views

urlpatterns = [
    path('add-delivery-address',views.add_delivery_address,name='add_delivery_address'),
    path('checkout',views.checkout,name='checkout'),
    path('cart',views.cart,name='cart'),
    path('add-to-cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('delete-cart/<int:id>',views.delete_cart,name="delete_cart"),
    path('apply-coin',views.apply_coin,name="apply_coin"),
    path('apply-coupon',views.apply_coupon,name="apply_coupon"),
    path('handlerequest',views.handlerequest,name="handlerequest"),
    path('orderConfirmed',views.orderConfirmed,name="orderConfirmed"),
    path('edit-delivery-address',views.edit_delivery_address,name="edit-delivery-address"),
]
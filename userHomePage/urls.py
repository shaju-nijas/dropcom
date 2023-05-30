from django.urls import path
from userHomePage import views

urlpatterns = [
    path('',views.index,name='index'),
    path('user-home-page',views.home,name='home'),
    path('products/<int:id>',views.products,name='products-list'),
    path('product-details/<int:id>',views.product_details,name='product-details'),
]
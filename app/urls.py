from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.home , name='home'),
    path('cart/' , views.view_cart , name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view_product/' , views.view_product , name="view_item"),
    path('customer_address/' , views.address , name='address')
    
]
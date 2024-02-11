from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.home , name='home'),
    path('cart/' , views.View_cart.as_view() , name='cart'),
    path('add_to_cart/<int:product_id>/', views.Add_to_cart.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view_product/' , views.view_product , name="view_item"),
    path('register/'  , views.Signup.as_view() , name='register'),
    path('login/' , views.Login.as_view()  , name='login'),
    path('logout/' , views.Logout.as_view()  , name='logout'),
    path('password_reset/' , views.PasswordReset.as_view()  , name='password_reset'),
    path('otp/<str:email>/' , views.OtpSystem.as_view()  , name='otp'),
    path('password_change/<str:email>/' , views.PasswordChange.as_view()  , name='password_change'),
    path('address/' , views.ConfirmOrder.as_view()  , name='address'),
    path("order_success/" , views.Order_success.as_view() , name="order_success" ),
    path("orders/" , views.ordersPage, name="orders" )
    
]
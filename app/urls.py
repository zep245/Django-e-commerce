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
    path('password_reset/' , views.passwordReset  , name='password_reset'),
    path('password_change/<str:token>/' , views.passwordChange  , name='password_change'),
    path('address/' , views.ConfirmOrder.as_view()  , name='address'),
    path("orders/" , views.Order_page.as_view(), name="orders" )
    
]
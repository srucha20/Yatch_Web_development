from django.urls import path 
from .views import *

app_name = 'src'

urlpatterns = [
    path('' , home , name="home") ,
    path('user-login/' , user_login , name="login") ,
    path('user-logout/' ,user_logout , name="logout") ,
    path('seller-register/' , seller_register , name="seller-register") ,    
    path('seller-dashboard/' , seller_dashboard , name="seller-dashboard") ,
    path('booked-yacht/' , booked_yacht , name="booked-yacht") ,
    path('add-yacht/'  , add_yacht , name="add-yacht")  ,
    path('customer-register/' , customer_register , name="customer-register") ,
    path('yacht-form/<int:pk>/' , yacht_form , name="yacht-form") ,
    path('customer-profile/' , customer_profile , name="customer-profile") ,
    
]
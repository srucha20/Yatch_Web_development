from src.models import *


def check_users(request):
    if request.user.is_authenticated:
        is_seller = False
        is_customer = False
        get_seller=seller.objects.filter(user=request.user)
        get_customer= customer.objects.filter(user=request.user)

        if get_seller:
            is_seller = True
        if get_customer:
            is_customer = True
        context={
            'seller':is_seller ,
            'customer':is_customer
        }    
        return context 
    else:
        pass        


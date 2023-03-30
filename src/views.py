from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate,logout as deauth, login  as dj_login
from .models import *
from django.conf import settings 
from django.core.mail import send_mail
from .forms import yacht_detailsForm
from django.template.loader import render_to_string
# Create your views here.



def home(request):
    yachtes=yacht_details.objects.all()
    context={
        'yachtes':yachtes
    }
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
            'yachtes':yachtes,
            'seller':is_seller ,
            'customer':is_customer
        }    
    return render(request , 'home.html',  context)

def user_login(request):
    if request.POST:
        get_email = request.POST.get('username')
        get_pass = request.POST.get('password1')

        if User.objects.filter(username=get_email).exists():
            user = authenticate(username=get_email , password=get_pass)
            if user:
                dj_login(request , user)
                messages.success(request , 'Logged in successfully')
                return redirect('src:home')
            else:
                messages.success(request , 'please enter correct password')
                return redirect('src:login')
        else:
            messages.success(request , 'This email is not registerd or incorrect')
            return redirect('src:login')

    return render(request , 'login.html')

def seller_register(request):
    if request.POST:
        get_email = request.POST.get('username')
        get_name = request.POST.get('name')
        get_pass1 = request.POST.get('password1')
        get_pass2 = request.POST.get('password2')

        if not get_email  and not get_name  and not get_pass1:
            messages.success(request , 'All fields are mandotry')
            return redirect('src:seller-register')
        
        if User.objects.filter(username=get_email).exists():
            messages.success(request , 'Email Alreday Exist')
            return redirect('src:seller-register')

        if get_pass1 != get_pass2 :
            messages.success(request , 'password did not matched')
            return redirect('src:seller-register')    

        get_user=User.objects.create(username=get_email)
        get_user.set_password(get_pass1)
        get_user.save()

        seller.objects.create(
            user=get_user ,
            name= get_name
        )
        user = authenticate(username=get_email , password=get_pass1)
        dj_login(request , user)
        messages.success(request , 'Account created successfully')
        return redirect('src:home')


    return render(request , 'seller-register.html')

def customer_register(request):
    if request.POST:
        get_email = request.POST.get('username')
        get_name = request.POST.get('name')
        get_phone = request.POST.get('phone')
        get_price = request.POST.get('price')
        get_pass1 = request.POST.get('password1')
        get_pass2 = request.POST.get('password2')

        if not get_email  and not get_name  and not get_pass1:
            messages.success(request , 'All fields are mandotry')
            return redirect('src:seller-register')
        
        if User.objects.filter(username=get_email).exists():
            messages.success(request , 'Email Alreday Exist')
            return redirect('src:seller-register')


        if get_pass1 != get_pass2 :
            messages.success(request , 'password did not matched')
            return redirect('src:seller-register')    

        get_user=User.objects.create(username=get_email)
        get_user.set_password(get_pass1)
        get_user.save()

        customer.objects.create(
            user=get_user ,
            name= get_name ,
            phone = get_phone ,
            price_range = get_price 

        )
        user = authenticate(username=get_email , password=get_pass1)
        dj_login(request , user)
        messages.success(request , 'Account created successfully')
        return redirect('src:home')
    
    return render(request , 'customer-register.html')




def user_logout(request):
    if request.user.is_authenticated:
        deauth(request)
    messages.success(request , "you are logout successfully")
    return redirect('src:home')


def seller_dashboard(request):
    if request.user.is_authenticated:
        get_user = seller.objects.filter(user=request.user).first()
        if get_user:
            all_yachtes=yacht_details.objects.filter(seller_id = get_user)
            return render(request , 'seller-dash.html' , {'yachtes':all_yachtes})
        else:
            messages.success(request , 'You are not a seller ')
            return redirect('src:home')
    else:
        messages.success(request , 'Login First')  
        return redirect('src:login')  

def add_yacht(request):
    if request.user.is_authenticated:
        get_user = seller.objects.filter(user=request.user).first()
        if get_user:
            if request.POST:
                form=yacht_detailsForm(request.POST , request.FILES)
                if form.is_valid():
                    get_f=form.save(commit=False)
                    get_f.seller_id = get_user
                    get_f.save()
                    messages.success(request , "Yacht Added Successfully")
                    return redirect('src:seller-dashboard')
            return render(request , 'add-yacht.html')
        else:
            messages.success(request , 'You are not a seller ')
            return redirect('src:home')
    else:
        messages.success(request , 'Login First')  
        return redirect('src:login')  

def yacht_form(request , pk):
    if request.user.is_authenticated:
        get_user = customer.objects.filter(user=request.user).first()
        if get_user:
            get_yacht = yacht_details.objects.filter(id=pk).first()  
            if request.POST:
                get_weeks = request.POST.get('rent_weeks')
                if not get_weeks:
                    messages.success(request , 'Plaese enter weeks first')
                    return redirect('src:yacht-form' , get_yacht.id)
                
                yacht_id=yacht_details.objects.filter(id=request.POST.get('yacht')).first()
                if book_yatch.objects.filter(yacht_details_id=yacht_id , customer_id=get_user).exists():
                    messages.success(request , 'You have alredy booked this yacht')
                    return redirect('src:yacht-form' , get_yacht.id)
                
                book_yatch.objects.create(
                            yacht_details_id = yacht_id ,
                            customer_id = get_user ,
                            rent_weeks = get_weeks ,
                            price = int( int(get_weeks)* yacht_id.rent_price  )
                )
                message_name="New Booking created"
                meassage_email= get_user.user.username   
                fullmessage="Someone created order for your yacht"
                data={
                    'name':message_name ,
                    'email': meassage_email ,
                    'content':fullmessage ,
                    'phone': get_user.phone 
                }
                html = render_to_string("cont.html" , data)
                send_mail(
                    message_name, 
                    fullmessage ,
                    meassage_email,
                    ['mawazid1051@gmail.com'],
                    html_message=html ,
                    fail_silently=False,
                )
                
                send_mail(
                    message_name, 
                    fullmessage ,
                    meassage_email,
                    ['mawazid1051@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request , "Yacht Booked Successfully")
                return redirect('src:home')  
            return render(request , 'yacht-form.html' , {'i':get_yacht})
        
        else:
            messages.success(request , 'You are not a customer ')
            return redirect('src:home')
    else:
        messages.success(request , 'Login First')  
        return redirect('src:login')  
    

def booked_yacht(request):
    if request.user.is_authenticated:
        get_user = seller.objects.filter(user=request.user).first()
        if get_user:
            books=book_yatch.objects.filter(yacht_details_id__seller_id=get_user)
            return render(request , 'booked-yacht.html' , {'books':books})
        else:
            messages.success(request , 'You are not a seller ')
            return redirect('src:home')
    else:
        messages.success(request , 'Login First')  
        return redirect('src:login')  


def customer_profile(request):
    if request.user.is_authenticated:
        get_user = customer.objects.filter(user=request.user).first()
        if get_user:
            bookings=book_yatch.objects.filter(customer_id=get_user)
            return render(request , 'customer-profile.html' , {'customer':get_user ,'bookings':bookings })
        
        else:
            messages.success(request , 'You are not a customer ')
            return redirect('src:home')
    else:
        messages.success(request , 'Login First')  
        return redirect('src:login')  


   


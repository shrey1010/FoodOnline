from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from .utils import detectUser,send_verfication_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor
from django.template.defaultfilters import slugify
from orders.models import Order
import datetime


# Create your views here.

#Restrict user to access only their dashboard
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            #send email to user to confirmation
            mail_subject = 'Activation Email'
            email_template = "accounts/emails/email_verification.html"
            send_verfication_email(request,user,mail_subject,email_template)

            messages.success(request, 'Your account has registered successfully!')
            messages.success(request, 'Verification mail has been sent to your email address. Please wait for the confirmation')
            return redirect('myAccount')
        else :
            print("Invalid Form")
    else:
        form = UserForm()
    context = { 
            'form': form,
        }
    return render(request,'accounts/registerUser.html',context = context )


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user = user)
            vendor.user_profile = user_profile
            vendor.save()
            
            #send email to user to confirmation

            mail_subject = 'Activation mail'
            email_template = "accounts/emails/email_verification.html"
            send_verfication_email(request,user,mail_subject,email_template)

            messages.success(request, 'Your Restaurant has registered successfully! Please wait for application confirmation .')
            return redirect('myAccount')
        else :
            print("Invalid Form")
    else:
        
        form = UserForm()
        v_form = VendorForm()

    context = {
            'form': form,
            'v_form': v_form,
        }
    return render(request,'accounts/registerVendor.html',context = context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myAccount')
    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, "you are logged in successfully")
            return redirect('myAccount')

        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out successfully")
    return redirect("login")

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectURL = detectUser(user)
    return redirect(redirectURL)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders = Order.objects.filter(user = request.user,is_ordered = True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
    }
    return render(request,'accounts/custDashboard.html',context=context)   
 
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user = request.user)
    orders= Order.objects.filter(vendors__in=[vendor.id],is_ordered = True).order_by('-created_at')
    recent_orders = orders[:5]

    # current month revenue 
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(vendors__in=[vendor.id],is_ordered = True,created_at__month = current_month)
    current_month_revenue = 0
    for order in current_month_orders:
        current_month_revenue += order.get_total_by_vendor()['grand_total']

    #total revenue 
    total_revenue = 0
    for order in orders:
        total_revenue += order.get_total_by_vendor()['grand_total']

    context={
        'vendor': vendor,
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }

    return render(request,'accounts/vendorDashboard.html',context = context) 



def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
    


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            mail_subject = 'Reset Your Password'
            email_template = "accounts/emails/reset_password_email.html"
            send_verfication_email(request,user,mail_subject,email_template)
            messages.success(request, 'Password reset link has been sent to your email address. Please wait for the confirmation')
            return redirect('myAccount')
        else :
            messages.error(request, "Account does not exist")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')

def reset_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()

            messages.success(request, "Password Changed Successfully!")
            redirect("myAccount")

        else :
            messages.error(request, "Password do not match")
            redirect('reset_password')
    return render(request, 'accounts/reset_password.html')



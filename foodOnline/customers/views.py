from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm,UserInfoForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from  django.contrib import messages
from orders.models import Order,OrderedFood
import simplejson as json

# Create your views here.

@login_required(login_url='login')
def cprofile(request):

    profile =   get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        user_form = UserInfoForm(request.POST,instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'profile updated successfully')

        else:
            messages.error(request,'AN error occured while updating your profile')


    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }

    

    return render(request, 'customers/cprofile.html',context=context)


def my_orders(request):
    orders = Order.objects.filter(user = request.user,is_ordered = True).order_by('-created_at')
    context = {
        'orders': orders,
        'orders_count': orders.count(),
    }
    return render(request,'customers/my_orders.html',context=context)


def order_detail(request,order_number):
    try:
        subtotal = 0
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        for item in ordered_food:
            subtotal += (item.price * item.quantity)

        tax_dict = json.loads(order.tax_data)
        context = {
        'order':order,
        'orderd_food':ordered_food,
        'subtotal':subtotal,
        'tax_dict':tax_dict,
        
        }
        return render(request,'customers/order_detail.html',context=context)

    except Exception as e:
        print(e)
        return redirect('custDashboard')
    
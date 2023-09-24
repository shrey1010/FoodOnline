from django.shortcuts import render
import simplejson as json
from orders.models import Order,OrderedFood
from .forms import VendorForm,OpeningHourForm
from accounts.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from .models import Vendor,OpeningHour
from django.contrib import messages 
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test,login_required
from accounts.views import check_role_vendor
from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'User Details updated')
            return redirect('vprofile')
        
        else:
            print("error in saving user details")
    
    else :
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "profile": profile,
        "vendor": vendor
    }
    return render(request, 'vendor/vprofile.html', context=context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menuBuilder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }
    return render(request,'vendor/menuBuilder.html',context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category,pk=pk)
    
    fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request,'vendor/fooditems_by_category.html',context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_Category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category added successfully!')
            return redirect('menuBuilder')
        else:
            print(form.errors)
        
    else:

        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request,'vendor/add_Category.html',context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_Category(request, pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category updated successfully!')
            return redirect('menuBuilder')
        else:
            print(form.errors)
        
    else:

        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request,'vendor/edit_Category.html',context=context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_Category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfully!')
    return redirect('menuBuilder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_Food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title'] 
            food = form.save(commit=False)
            food.vendor = Vendor.objects.get(user=request.user)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request,'Food item added successfully!')
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
        
    else:

        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=Vendor.objects.get(user=request.user))
    context = {
        'form': form,
    }
    return render(request,'vendor/add_Food.html',context=context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_Food(request, pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title'] 
            food = form.save(commit=False)
            food.vendor = Vendor.objects.get(user=request.user)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request,'Food item Updated successfully!')
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
        
    else:

        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=Vendor.objects.get(user=request.user))
    context = {
        'form': form,
        'food': food,
    }
    return render(request,'vendor/edit_Food.html',context=context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_Food(request,pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request,'Food Item has been deleted successfully!')
    return redirect('fooditems_by_category',food.category.id)


def opening_hours(request):
    vendor = Vendor.objects.get(user=request.user)
    opening_hours = OpeningHour.objects.filter(vendor=vendor)
    
    form = OpeningHourForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'vendor/opening_hours.html', context=context)



def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.method == 'POST':
                day = request.POST.get('day')
                from_hour = request.POST.get('from_hour')
                to_hour = request.POST.get('to_hour')
                is_closed = request.POST.get('is_closed')
                try:
                    vendor = Vendor.objects.get(user=request.user)
                    hour = OpeningHour.objects.create(vendor=vendor, day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                    if hour:
                        day = OpeningHour.objects.get(id=hour.id)
                        if day.is_closed:
                            response = {
                                'status': 'success',
                                'id': hour.id,
                                'day': day.get_day_display(),
                                'is_closed': 'Closed',
                            }
                        else:
                            response = {
                                'status': 'success',
                                'id': hour.id,
                                'day': day.get_day_display(),
                                'from_hour': hour.from_hour,
                                'to_hour': hour.to_hour,
                            }
                    return JsonResponse(response)
                except IntegrityError as e:
                    response = {'status': 'Failed', 'message': from_hour+'-'+to_hour+' is already exits for this day!'}
                    return JsonResponse(response)
                
        else:
            HttpResponse('Invalid Request ')


def remove_opening_hours(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour,pk=pk)
            if hour:
                hour.delete()
                response = {'status': 'success','id':pk, 'message': 'Opening Hour has been deleted successfully!'} 
                return JsonResponse(response)
            response = {'status':'failed', 'message': 'Time Duration is not Found'}
            return JsonResponse(response)

        response = {'status':'failed', 'message': 'Invalid Request!'}
        return JsonResponse(response)

    response = {'status':'failed', 'message': 'User is not authenticated'}
    return JsonResponse(response)

def order_detail(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        vendor = Vendor.objects.get(user=request.user)
        ordered_food = OrderedFood.objects.filter(order=order,fooditem__vendor=vendor)
        context = {
        'order':order,
        'orderd_food':ordered_food,
        'subtotal':order.get_total_by_vendor()['subtotal'],
        'tax_dict':order.get_total_by_vendor()['tax_dict'],
        'grand_total':order.get_total_by_vendor()['grand_total'],
        }
        return render(request,'vendor/order_detail.html',context=context)

    except Exception as e:
        print(e)
        return redirect('vendorDashboard')
    

def my_order(request):
    vendor = Vendor.objects.get(user = request.user)
    orders= Order.objects.filter(vendors__in=[vendor.id],is_ordered = True).order_by('-created_at')
    context={
        'orders': orders
    }
    return render(request,'vendor/my_order.html',context=context)

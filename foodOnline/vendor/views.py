from django.shortcuts import render
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages 
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test,login_required
from accounts.views import check_role_vendor
from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify


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

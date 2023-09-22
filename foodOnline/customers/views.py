from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm,UserInfoForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from  django.contrib import messages

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

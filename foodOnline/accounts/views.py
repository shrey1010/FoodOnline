from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
from .models import User
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            return HttpResponse('User Created')
    else:
        form = UserForm()
        context = { 
            'form ': form,
        }
        return render(request,'accounts/registerUser.html',context = context )
        form = UserForm 
        context = {
            'form ': form,
        }
        return render(request,'accounts/registerUser.html',context = context )



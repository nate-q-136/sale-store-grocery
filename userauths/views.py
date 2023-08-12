from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
import traceback
from .models import User

# User = settings.AUTH_USER_MODEL
# Create your views here.

def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            # cleaned_data là 1 thuộc tính đã đc validate từ form
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hello {username}, your account was created successfully!')
            # authenticate: use username and password as default params to authenticate
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
    
            # login(request,new_user)
            # redirect(<app_name>:<def name>)
            return redirect('userauths:sign-in')
        
        pass
    else:
        form = UserRegisterForm()
    
    context = {
        'form':form,
    }
    return render(request, 'userauths/sign-up.html',context=context)


def login_view(request):
    context={
        
    }
    if request.user.is_authenticated:
        print(request.user)
        print(request.user.is_authenticated)
        context = {
            'user':request.user
        }
        return render(request,'core/index.html',context)
    if request.method == 'POST':
        # nhớ là get name của input
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request=request, email=email, password=password)
        
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged in")
                context = {
                    'user':user
                }
                
                return render(request,"core/index.html",context)
            else:
                print("no vo day")
                messages.warning(request, f"User does not exist. Create a new account")
                
            
        except:
            traceback.print_exc()
            messages.warning(request, f"User with {email} does not exist")
            pass
        
    
    return render(request, 'userauths/sign-in.html', context)
    pass


def logout_view(request):
    logout(request=request)
    # messages.success(request, "You have logged out")
    return redirect("userauths:sign-in")
    # return render(request,"core/index.html")
    pass
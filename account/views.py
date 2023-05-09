from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# from .models import User
from .forms import UserSignupForm, UserLoginForm
from .models import Profile


# Create your views here.


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            form = UserLoginForm()
    else:
        form = UserLoginForm()
    
    return render(request, 'account/signin/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def sign_up(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            try:
                profile = Profile.objects.get(user=user.pk)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)
            
            profile.username = form.cleaned_data.get('username')
            profile.save()
            
            login(request, user)
            return redirect('home')
            
            
    else:
        form = UserSignupForm()
    
    return render(request, 'account/signup/signup.html', {'form': form})




@login_required
def update_profile(request, id):
    
    submitted = False
    
    if request.method == "POST":
        
        submitted = True
        
        new_nickname = request.POST.get('username')
        
        if new_nickname:
            
            Profile.objects.filter(user=id)\
                .update( nickname = new_nickname )
        
    profile = Profile.objects.get(user=id)
    
    return render(request, 'account/profile/update.html', {
        "profile": profile, 
        "submitted": submitted, 
    })











































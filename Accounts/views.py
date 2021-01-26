from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Profile
from django.contrib.auth import authenticate, login
from .decorators import unathenticated_user
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@login_required
def dashboard(request):
    return render(request, 'Accounts/dashboard.html')


@login_required
def profile_view(request, username):
    user = get_object_or_404(User,
                            username=username,
                            is_active=True)
    return render(request, 'Accounts/view_profile.html', 
                {'user':user})


@unathenticated_user
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            profile.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return redirect('Accounts:edit_profile')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'Accounts/register.html',
                  {'user_form':user_form})
    
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            print('updated')
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, "Accounts/edit_profile.html", {'profile_form':profile_form})
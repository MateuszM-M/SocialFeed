from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Profile
from django.contrib.auth import authenticate, login
from .decorators import unathenticated_user
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from Posts.models import Post
from Posts.forms import PostForm


@login_required
def dashboard(request):
    posts = Post.objects.all()
    post_form = PostForm
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
        return redirect('/')
    return render(request, 'Accounts/dashboard.html', {'posts':posts,
                                                       'post_form':post_form})


@login_required
def profile_view(request, username):
    posts = Post.objects.filter(user__username=username)
    user = get_object_or_404(User,
                            username=username,
                            is_active=True)
    return render(request, 'Accounts/view_profile.html', 
                {'user':user,
                 'posts':posts})
    
    

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
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, "Accounts/edit_profile.html", {'profile_form':profile_form})
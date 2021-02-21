from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from Posts.forms import PostForm, CommentForm
from Posts.models import Post, Comment

from .decorators import unathenticated_user
from .forms import *
from .models import Contact, Profile


@login_required
def dashboard(request):
    friends = request.user.profile.friends.all()
    posts = Post.objects.filter(Q(user__in=friends) | Q(user=request.user))
    paginator_p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator_p.get_page(page_number)
    post_form = PostForm
    comment_form = CommentForm
    
    context = {'posts': posts, 'post_form': post_form,
               'comment_form': comment_form}
    return render(request, 'Accounts/dashboard.html', context)



@login_required
def profile_view(request, username):
    user = Profile.objects.get(user__username=username)
    friends = user.friends.all()[:6]

    posts = Post.objects.filter(user__username=username)
    paginator_p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator_p.get_page(page_number)

    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    my_invites = Contact.objects.invitations_received(request.user.profile)
    invited = Contact.objects.filter(sender=request.user.profile, 
                                     receiver=user.profile)

    title = user
    
    comment_form = CommentForm

    contacts = []
    for i in invited:
        contacts.append(request.user.profile)
        
    context = {'user': user,
               'title': user,
               'posts': posts,
               'friends': friends,
               'contacts': contacts,
               'my_invites': my_invites,
               'comment_form': comment_form}
        
    return render(request, 'Accounts/view_profile.html', context)


@login_required()
def users_friends(request, username):
    user = Profile.objects.get(user__username=username)
    friends = user.friends.all()
    paginator = Paginator(friends, 16)
    page_number = request.GET.get('page')
    friends = paginator.get_page(page_number)
    return render(request, 'Accounts/friend_list.html',
                  {'friends': friends})


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
                  {'user_form': user_form})


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
    return render(request, "Accounts/edit_profile.html", 
                  {'profile_form': profile_form})


@login_required
def invite(request, username):
    if request.method == 'POST':
        sender = Profile.objects.get(user=request.user)
        user = get_object_or_404(User,
                                 username=username,
                                 is_active=True)
        receiver = Profile.objects.get(user=user)
        contact = Contact.objects.create(sender=sender, receiver=receiver)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('Accounts:dashboard')


@login_required
def accept(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        sender = Profile.objects.get(user__username=user)
        receiver = Profile.objects.get(user=request.user)
        contact = get_object_or_404(Contact, sender=sender, receiver=receiver)
        contact.status = 'accepted'
        contact.save()
        contact.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('Accounts:dashboard')


@login_required
def reject(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        sender = Profile.objects.get(user__username=user)
        receiver = Profile.objects.get(user=request.user)
        contact = get_object_or_404(Contact, sender=sender, receiver=receiver)
        contact.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('Accounts:dashboard')


@login_required
def delete_friend(request, username):
    deleter = Profile.objects.get(user=request.user)
    deleted_friend = Profile.objects.get(user__username=username)
    if request.method == 'POST':
        deleter.friends.remove(deleted_friend.user)
        deleted_friend.friends.remove(deleter.user)
        return redirect('Accounts:dashboard')
    return render(request, 'Accounts/delete_friend.html', 
                  {'deleted_friend': deleted_friend,
                   'deleter': deleter})


@login_required()
def profile_search(request):
    query = request.GET.get('search')
    if query:
        results = User.objects.annotate(
            search=SearchVector('username'),
        ).filter(search=query)
        return render(request, 'Accounts/search.html',
                      {'query': query,
                       'results': results})


@login_required()
def recommended_users(request):
    people = Profile.objects.exclude(
        user=request.user
        ).order_by('date_created')[:10:-1]
    paginator = Paginator(people, 8)
    page_number = request.GET.get('page')
    people = paginator.get_page(page_number)
    return render(request, 'Accounts/people.html',
                  {'people': people})

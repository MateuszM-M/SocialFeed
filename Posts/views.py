from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.http import HttpResponseRedirect
from datetime import datetime
from django.utils.timezone import now


@login_required
def post_view(request, username, pk, slug):
    post = get_object_or_404(Post, user__username=username, id=pk, slug=slug)
    return render(request, 'Posts/post_details.html', {'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.user == request.user:
        if request.method == 'POST':
            post.delete()
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'Posts/remove_post.html', {'post': post})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.user == request.user:
        if request.method == 'POST':
            post_edit_form = PostForm(data=request.POST, instance=post)
            if post_edit_form.is_valid():
                post_edit_form.save(commit=False)
                post.updated_date = datetime.now()
                post_edit_form.save()
                return redirect('/')
        else:
            post_edit_form = PostForm(instance=post)
    else:
        return redirect('/')
    return render(request, 'Posts/edit_post.html', {'post_edit_form': post_edit_form,
                                                    'post': post})
    
    
@login_required  
def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.users_like.filter(id=request.user.id).exists():
        post.users_like.remove(request.user)
        liked = False
    else:
        post.users_like.add(request.user)
        liked = True
    post.total_likes = post.users_like.all().count()
    post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

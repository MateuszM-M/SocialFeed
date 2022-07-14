from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from .forms import PostForm, CommentForm
from django.http import HttpResponseRedirect
from datetime import datetime


@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
        return redirect('/')


@login_required
def post_view(request, username, pk, slug):
    post = get_object_or_404(Post, user__username=username, id=pk, slug=slug)
    comment_form = CommentForm
    return render(request, 'Posts/post_details.html',
                  {'post': post,
                   'comment_form': comment_form})


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
    return render(request, 'Posts/edit_post.html',
                  {'post_edit_form': post_edit_form, 'post': post})
    
    
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    next_url = request.POST.get('next', '/')
    if request.method == 'POST':
        if post.users_like.filter(id=request.user.id).exists():
            post.users_like.remove(request.user)
        else:
            post.users_like.add(request.user)
    Post.total_likes_count(post)
    return HttpResponseRedirect(next_url)


@login_required
def add_comment(request, pk):
    next_url = request.POST.get('next', '/')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = Post.objects.get(id=pk)
            new_comment.save()
        return HttpResponseRedirect(next_url)


@login_required
def remove_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if comment.author == request.user:
        if request.method == 'POST':
            comment.delete()
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'Posts/remove_comment.html', {'comment': comment})


@login_required
def edit_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if comment.author == request.user:
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('/')
        else:
            comment_form = CommentForm(instance=comment)
    else:
        return redirect('/')
    return render(request, 'Posts/edit_comment.html',
                  {'comment_form': comment_form,
                   'comment': comment})


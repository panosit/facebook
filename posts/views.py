from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Like


@login_required
def feed(request):
    from friends.models import FriendRequest
    friends = FriendRequest.objects.filter(
        status='accepted',
        from_user=request.user
    ).values_list('to_user', flat=True) | FriendRequest.objects.filter(
        status='accepted',
        to_user=request.user
    ).values_list('from_user', flat=True)

    posts = Post.objects.filter(author__in=friends) | Post.objects.filter(author=request.user)
    posts = posts.select_related('author').prefetch_related('likes', 'comments').distinct()

    return render(request, 'posts/feed.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            post = Post.objects.create(
                author=request.user,
                content=content
            )
            if request.FILES.get('image'):
                post.image = request.FILES['image']
                post.save()
            messages.success(request, 'Post created!')
        else:
            messages.error(request, 'Post content cannot be empty.')
    return redirect('feed')


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('feed')


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Comment added!')
    return redirect('feed')


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('feed')

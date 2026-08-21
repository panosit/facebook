from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import FriendRequest
from .utils import get_friend_ids

User = get_user_model()


@login_required
def send_friend_request(request, user_id):
    if user_id == request.user.id:
        messages.warning(request, "You can't add yourself as a friend.")
        return redirect('profile', username=request.user.username)

    to_user = get_object_or_404(User, id=user_id)

    existing = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=to_user
    ).first()

    if existing:
        if existing.status == 'pending':
            messages.info(request, "Friend request already sent.")
        elif existing.status == 'accepted':
            messages.info(request, "You're already friends.")
        elif existing.status == 'rejected':
            existing.status = 'pending'
            existing.save()
            messages.success(request, "Friend request resent.")
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, f"Friend request sent to {to_user.username}!")

    return redirect('profile', username=to_user.username)


@login_required
def respond_to_request(request, request_id, action):
    friend_req = get_object_or_404(FriendRequest, id=request_id)
    if friend_req.to_user != request.user:
        messages.error(request, "You can't respond to this request.")
        return redirect('directory')

    if action == 'accept':
        friend_req.status = 'accepted'
        friend_req.save()
        messages.success(request, f"You're now friends with {friend_req.from_user.username}!")
    elif action == 'reject':
        friend_req.status = 'rejected'
        friend_req.save()
        messages.info(request, "Friend request rejected.")

    return redirect('friend_requests')


@login_required
def friend_requests(request):
    pending = FriendRequest.objects.filter(to_user=request.user, status='pending')
    return render(request, 'friends/requests.html', {'pending_requests': pending})


@login_required
def my_friends(request):
    friend_ids = get_friend_ids(request.user)
    friends_qs = User.objects.filter(id__in=friend_ids)
    return render(request, 'friends/my_friends.html', {'friends': friends_qs})


@login_required
def remove_friend(request, user_id):
    to_remove = get_object_or_404(User, id=user_id)

    FriendRequest.objects.filter(
        from_user=request.user,
        to_user=to_remove,
        status='accepted'
    ).delete()

    FriendRequest.objects.filter(
        from_user=to_remove,
        to_user=request.user,
        status='accepted'
    ).delete()

    messages.success(request, f"{to_remove.username} removed from friends.")
    return redirect('my_friends')

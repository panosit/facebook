from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Poke, UserProfile
from friends.utils import get_friend_ids, get_network_stats

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('directory')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('directory')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('directory')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('directory')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def about(request):
    return render(request, 'accounts/about.html')


@login_required
def directory(request):
    users = User.objects.exclude(id=request.user.id).select_related('profile')
    query = request.GET.get('q', '').strip()
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(profile__concentration__icontains=query) |
            Q(profile__house__icontains=query) |
            Q(profile__courses__icontains=query)
        )
    return render(request, 'accounts/directory.html', {'users': users, 'query': query})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    friend_ids = get_friend_ids(profile_user)
    friends_qs = User.objects.filter(id__in=friend_ids)
    network_stats = get_network_stats(profile_user)
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'profile_friends': friends_qs,
        'network_stats': network_stats,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()

        profile = request.user.profile
        profile.concentration = request.POST.get('concentration', '')
        profile.house = request.POST.get('house', '')
        profile.class_year = request.POST.get('class_year') or None
        profile.relationship_status = request.POST.get('relationship_status', '')
        profile.interested_in = request.POST.get('interested_in', '')
        profile.courses = request.POST.get('courses', '')
        profile.about_me = request.POST.get('about_me', '')

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile', username=request.user.username)

    return render(request, 'accounts/edit_profile.html', {'user': request.user})


@login_required
def classmates(request, course):
    classmates_qs = UserProfile.objects.filter(
        courses__icontains=course
    ).exclude(user=request.user).select_related('user')
    return render(request, 'accounts/classmates.html', {
        'course': course,
        'classmates': classmates_qs,
    })


@login_required
def send_poke(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if to_user == request.user:
        messages.warning(request, "You can't poke yourself.")
    else:
        Poke.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, f"You poked {to_user.username}!")
    return redirect('profile', username=to_user.username)


@login_required
def pokes_view(request):
    received = Poke.objects.filter(to_user=request.user)
    return render(request, 'accounts/pokes.html', {'received': received})


@login_required
def remove_poke(request, poke_id):
    poke = get_object_or_404(Poke, id=poke_id, to_user=request.user)
    poke.delete()
    return redirect('pokes')

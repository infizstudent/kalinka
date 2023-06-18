from django.contrib.auth.models import User
from .forms import UserProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile(request):
    user_profile = request.user.userprofile
    return render(request, 'vebschet/profile.html', {'user_profile': user_profile})


def index(request):
    return render(request, 'vebschet/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Вы можете войти в систему.')
            return redirect('profile', username=username)
    else:
        form = UserRegisterForm()
    return render(request, 'vebschet/register.html', {'form': form})

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'form': form})


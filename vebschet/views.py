from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from vebschet.models import UserProfile
from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm
from django.contrib.auth.views import LoginView
from django.urls import reverse


@login_required
def profile(request, username):
    if username != request.user.username:
        return redirect('profile', username=request.user.username)
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save()

            if request.is_ajax():
                data = {
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'patronymic': user_profile.patronymic,
                    'field': user_profile.field,
                    'counter': user_profile.counter,
                }
                return HttpResponse(json.dumps(data), content_type='application/json')

            return redirect('profile', username=username)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile.html', {'form': form, 'user_profile': user_profile})


class CustomLoginView(LoginView):
    def get_success_url(self):
        username = self.request.user.username
        return reverse('profile', args=[username])


def index(request):
    return render(request, 'vebschet/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # Создание UserProfile при регистрации
            username = form.cleaned_data.get('username')
            login(request, user)  # войти в систему после регистрации
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('profile', username=username)
    else:
        form = UserRegisterForm()
    return render(request, 'vebschet/register.html', {'form': form})

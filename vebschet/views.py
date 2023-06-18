from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.models import User
from vebschet.forms import UserRegisterForm, UserProfileForm
from django.shortcuts import render, redirect
from vebschet.models import UserProfile
from django.http import HttpResponse
import json
from django.contrib.auth import update_session_auth_hash
from .forms import UserPasswordChangeForm


@login_required
def profile(request, username):
    if username != request.user.username:
        return redirect('profile', username=request.user.username)
        # вместо этого вы можете вернуть HttpResponseForbidden, если хотите выдать ошибку 403

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
        return reverse('profile', args=[self.request.user.username])


def index(request):
    return render(request, 'vebschet/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile', username=user.username)
    else:
        form = UserRegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'vebschet/register.html', {'form': form, 'profile_form': profile_form})


@login_required
def password_change(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # обновляем сессию пользователя, чтобы избежать выхода из системы после смены пароля
            return redirect('profile', username=request.user.username)
        else:
            pass
    else:
        form = UserPasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})
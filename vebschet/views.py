from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from vebschet.models import UserProfile, MeterReading
from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm, MeterReadingForm
from django.contrib.auth.views import LoginView
from django.urls import reverse


@login_required
def profile(request, username):
    if username != request.user.username:
        return redirect('profile', username=request.user.username)
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'patronymic': user_profile.patronymic,
                    'field': user_profile.field,
                    'counter': user_profile.counter,
                }
                return HttpResponse(json.dumps(data), content_type='application/json')

            return redirect('counter', username=username)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile.html', {'form': form, 'user_profile': user_profile})


class CustomLoginView(LoginView):
    def get_success_url(self):
        username = self.request.user.username
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.first_name and user_profile.last_name and user_profile.patronymic and user_profile.field is not None and user_profile.counter is not None:
            return reverse('counter', args=[username])
        else:
            return reverse('profile', args=[username])


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('profile', username=username)
    else:
        form = UserRegisterForm()
    return render(request, 'vebschet/register.html', {'form': form})


@login_required
def counter_view(request, username):
    if username != request.user.username:
        return redirect('profile', username=request.user.username)

    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = MeterReadingForm(request.POST, initial={'user': user})
        if form.is_valid():
            meter_reading = form.save(commit=False)
            meter_reading.user = user
            meter_reading.counter = user_profile

            meter_reading.howireceive = "add from the system"

            meter_reading.save()
            return redirect('reading_list', username=username)
    else:
        form = MeterReadingForm(initial={'user': user})

    return render(request, 'vebschet/counter.html', {'form': form, 'username': username})



@login_required
def user_reading_list(request, username):
    if username != request.user.username:
        return redirect('profile', username=request.user.username)

    user = User.objects.get(username=username)
    meter_readings = MeterReading.objects.filter(user=user).order_by('-date')

    return render(request, 'vebschet/reading_list.html', {'meter_readings': meter_readings, 'username': username})


@login_required
def reading_list(request, username):
    if username != request.user.username:
        return redirect('profile', username=request.user.username)

    user = User.objects.get(username=username)
    meter_readings = MeterReading.objects.filter(user=user).order_by('-date')
    return render(request, 'vebschet/reading_list.html', {'meter_readings': meter_readings, 'username': username})


@login_required
def settings(request, username):
    if username != request.user.username:
        return redirect('profile', username=request.user.username)

    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('counter', username=username)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'vebschet/settings.html', {'form': form})


def index(request):
    return render(request, 'vebschet/index.html')

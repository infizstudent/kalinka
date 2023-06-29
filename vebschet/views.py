from .forms import UserRegisterForm, UserProfileForm, MeterReadingForm, ElectricityCoastCalculatorForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, MeterReading, ElectricityPrice
from django.contrib.auth.decorators import login_required
from .utils import get_user_profile, get_meter_readings
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
import json


def profile(request, username):
    user_profile = get_user_profile(request, username)

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
        user_profile = self.request.user.userprofile
        if all([user_profile.first_name, user_profile.last_name, user_profile.patronymic,
                user_profile.field is not None, user_profile.counter is not None]):
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
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('profile', username=username)
    else:
        form = UserRegisterForm()
    return render(request, 'vebschet/register.html', {'form': form})


@login_required
def counter_view(request, username):
    user_profile = get_user_profile(request, username)

    if request.method == 'POST':
        form = MeterReadingForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            meter_reading = form.save(commit=False)
            meter_reading.user = request.user
            meter_reading.counter = user_profile

            meter_reading.howireceive = "add from the system"

            meter_reading.save()
            return redirect('reading_list', username=username)
    else:
        form = MeterReadingForm(initial={'user': request.user})

    @property
    def formatted_date(self):
        return self.date.strftime('%Y-%m-%d')

    return render(request, 'vebschet/counter.html', {'form': form, 'username': username})


@login_required
def reading_list(request, username):
    get_user_profile(request, username)
    meter_readings = get_meter_readings(request)
    return render(request, 'vebschet/reading_list.html', {'meter_readings': meter_readings, 'username': username})


@login_required
def settings(request, username):
    user_profile = get_user_profile(request, username)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            for field in form.fields:
                if not form.cleaned_data[field]:
                    form.add_error(field, 'This field cannot be empty')
            if not form.errors:
                form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('counter', username=username)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'vebschet/settings.html', {'form': form})


@login_required
def electricity_price_view(request):
    electricity_price = get_object_or_404(ElectricityPrice, id=1)
    return render(request, 'vebschet/electricity_price.html', {'electricity_price': electricity_price})


@login_required
def electricity_coast_view(request):
    electricity_price = get_object_or_404(ElectricityPrice, id=1)
    total_coast = None
    consumption = None

    meter_readings = MeterReading.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = ElectricityCoastCalculatorForm(request.POST, user=request.user)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            start_reading = MeterReading.objects.filter(user=request.user, date__date=start_date).first()
            end_reading = MeterReading.objects.filter(user=request.user, date__date=end_date).first()

            if start_reading and end_reading:
                consumption = start_reading.reading - end_reading.reading
                total_coast = consumption * electricity_price.price
    else:
        form = ElectricityCoastCalculatorForm(user=request.user)

    return render(request, 'vebschet/electricity_coast.html', {
        'electricity_price': electricity_price,
        'form': form,
        'total_coast': total_coast,
        'consumption': consumption,
        'meter_readings': meter_readings
    })


def meter_reading_view(request):
    readings = MeterReading.objects.all()
    return render(request, 'meter_reading.html', {'readings': readings})


def index(request):
    return render(request, 'vebschet/index.html')

from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')
    else:
        form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'vebschet/registration.html', {'form': form, 'profile_form': profile_form})


@login_required
def profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'vebschet/profile.html', {'user': user, 'form': form})

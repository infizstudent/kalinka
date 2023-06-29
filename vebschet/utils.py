from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def get_user_profile(request, username):
    if username != request.user.username:
        return redirect('profile', username=request.user.username)
    return request.user.userprofile


@login_required
def get_meter_readings(request):
    return request.user.meterreading_set.order_by('-date')

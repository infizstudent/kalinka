from django.contrib import admin
from django.urls import path, include
from vebschet import views as vebschet_views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', vebschet_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='vebschet/profile.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='vebschet/logout.html'), name='logout'),
    path('profile/', vebschet_views.profile, name='profile'),
]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += staticfiles_urlpatterns()

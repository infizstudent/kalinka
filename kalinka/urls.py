from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from vebschet import views as vebschet_views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from vebschet.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', vebschet_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='vebschet/logout.html'), name='logout'),
    path('login/', CustomLoginView.as_view(template_name='vebschet/login.html'), name='login'),
    path('profile/<str:username>/', vebschet_views.profile, name='profile'),
    path('', vebschet_views.index, name='index'),
    path('set_language/', set_language, name='set_language'),
    path('password_change/', vebschet_views.password_change, name='password_change'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='vebschet/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='vebschet/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='vebschet/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='vebschet/password_reset_complete.html'),
         name='password_reset_complete'),

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += staticfiles_urlpatterns()

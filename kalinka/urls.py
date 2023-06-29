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
    path('counter/<str:username>/', vebschet_views.counter_view, name='counter'),
    path('reading_list/<str:username>/', vebschet_views.reading_list, name='reading_list'),
    path('settings/<str:username>/', vebschet_views.settings, name='settings'),
    path('electricity_coast/', vebschet_views.electricity_coast_view, name='electricity_coast'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += staticfiles_urlpatterns()

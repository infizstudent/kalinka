from django.contrib import admin
from .models import UserProfile, MeterReading


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'patronymic', 'field', 'counter']
    search_fields = ['user__username', 'first_name', 'last_name', 'patronymic']


@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ['user', 'reading', 'date']
    search_fields = ['user__username']
    list_filter = ['date']


from django.contrib import admin
from .models import UserProfile, MeterReading, ElectricityPrice


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'patronymic', 'field', 'counter']
    search_fields = ['user__username', 'first_name', 'last_name', 'patronymic']


@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_counter', 'reading', 'date')
    search_fields = ['user__username']
    list_filter = ['date']

    def get_user_counter(self, obj):
        return obj.counter.counter

    def get_date(self, obj):
        return obj.date.strftime('%Y-%m-%d')

    get_date.short_description = 'Date'  # Sets column name in admin panel

    get_user_counter.short_description = 'Counter'


class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)


admin.site.register(ElectricityPrice, SingletonModelAdmin)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, MeterReading


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use")
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'patronymic', 'field', 'counter']


class MeterReadingForm(forms.ModelForm):
    class Meta:
        model = MeterReading
        fields = ['reading']

    def clean_reading(self):
        new_reading = self.cleaned_data.get('reading')

        # Проверка на отрицательные значения и дробные числа
        if new_reading < 0 or not float(new_reading).is_integer():
            raise ValidationError("Please enter a non-negative whole number.")

        # Получение текущего пользователя
        user = self.initial.get('user')

        # Проверка, есть ли последний показатель счетчика
        try:
            last_reading = MeterReading.objects.filter(user=user).latest('date').reading
            if new_reading < last_reading:
                raise ValidationError("New reading is less than the last one.")
        except MeterReading.DoesNotExist:
            # Если показатели счетчика еще не существуют, возвращаем новое значение
            return new_reading
        return new_reading

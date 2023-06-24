from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, MeterReading
from datetime import datetime


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

        if new_reading < 0 or not float(new_reading).is_integer():
            raise ValidationError("Please enter a non-negative whole number.")

        user = self.initial.get('user')

        try:
            last_reading = MeterReading.objects.filter(user=user).latest('date').reading
            if new_reading < last_reading:
                raise ValidationError("New reading is less than the last one.")
        except MeterReading.DoesNotExist:
            return new_reading
        return new_reading


class ElectricityCoastCalculatorForm(forms.Form):
    start_date = forms.ChoiceField()
    end_date = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ElectricityCoastCalculatorForm, self).__init__(*args, **kwargs)
        date_choices = MeterReading.objects.filter(user=user).values_list('date', flat=True)
        date_choices = [(date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d')) for date in date_choices]
        self.fields['start_date'].choices = date_choices
        self.fields['end_date'].choices = date_choices
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            if start_date <= end_date:
                raise forms.ValidationError("Error: date start cannot be less than or equal to end.")
        return cleaned_data

# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Booking

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e)
        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'phone', 'address', 'preferred_datetime']
        widgets = {
            'preferred_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
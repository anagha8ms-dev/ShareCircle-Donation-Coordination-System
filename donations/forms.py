from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Donation, Profile
from django.contrib.auth import authenticate



class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES
    )

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    role = forms.ChoiceField(
        choices=[
            ('Donor', 'Donor'),
            ('Recipient', 'Recipient'),
        ],
        label='Login As'
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError("Invalid username or password.")

            cleaned_data['user'] = user

        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'title',
            'category',
            'description',
            'image',
            'condition',
            'location'
        ]
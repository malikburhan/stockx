from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder':'Re Enter Password'})

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')

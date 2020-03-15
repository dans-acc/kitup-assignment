from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from kitup.models import Users


class UserRegistrationForm(forms.ModelForm):
    First_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
    Last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))
    Confirm_Password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}))

    class Meta:
        model = User
        fields = ['username', 'email']

        # The following lines integrate the CSS/Bootstrap4 implementation in register.html using widgets

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'true', 'required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'true'}),
        }

    # The following function checks for the user password for validation

    def PassCheck(self):
        cd = self.cleaned_data
        if cd['Confirm_Password'] != cd['Password']:
            raise ValidationError("The passwords do not match!")

        return cd['Confirm_Password']

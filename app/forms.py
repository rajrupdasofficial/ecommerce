from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import CustomerProfile
from django.contrib.auth import authenticate
from django.utils.translation import gettext, gettext_lazy as _

"""registration form"""


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()  # Get the custom user model
        fields = ['email', 'password1', 'password2']
        labels = {'email': 'Email'}


"""login form"""


class LoginForm(AuthenticationForm):
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

    # error_messages = {
    #     'invalid_login': _("Please enter a correct email and password. Note that both "
    #                        "fields may be case-sensitive."),
    #     'inactive': _("This account is inactive."),
    # }

    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')

    #     if email is not None and password:
    #         self.user_cache = authenticate(
    #             self.request, email=email, password=password)
    #         if self.user_cache is None:
    #             raise self.get_invalid_login_error()
    #         else:
    #             self.confirm_login_allowed(self.user_cache)

    #     return self.cleaned_data


"""customer profile form"""


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ["name", "phonenumber",
                  "locality", "city", "zipcode", "state"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phonenumber': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }

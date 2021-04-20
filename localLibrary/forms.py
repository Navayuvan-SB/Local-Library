from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class CustomSignupForm(UserCreationForm):
    """Add first_name and last_name inputs on
        user creation"""

    first_name = forms.CharField(
        label=_("First name"),
        strip=True,
        help_text="Enter your first name",
        required=True
    )

    last_name = forms.CharField(
        label=_("Last name"),
        strip=True,
        help_text="Enter your last name",
        required=True
    )


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        field_classes = {'username': UsernameField}

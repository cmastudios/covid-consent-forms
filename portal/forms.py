from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import EmailField

from .models import Institution, InstitutionEmail


def check_email_in_institutions(email):
    for iemail in InstitutionEmail.objects.all():
        if email.endswith(iemail.email_suffix):
            return True
    raise ValidationError("Email does not belong to a member institution. Check capitalization / punctuation.")


class InstitutionForm(forms.Form):
    institution = forms.ModelChoiceField(Institution.objects)


class CreateUserForm(UserCreationForm):
    username = UsernameField(
        label="Username",
        strip=False,
        help_text="This should uniquely identify you and your institution",
        max_length=150
    )

    email = forms.EmailField(
        label="Email",
        initial="@health.slu.edu",
        help_text="Must be from a member institution. Will be verified.",
        validators=[check_email_in_institutions]
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)
        field_classes = {'username': UsernameField, 'email': EmailField}

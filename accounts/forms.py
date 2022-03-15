from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.models import Account


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-input', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-input', 'placeholder': 'Repeat your password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your LastName'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}))

    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'password1',
            'password2',
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

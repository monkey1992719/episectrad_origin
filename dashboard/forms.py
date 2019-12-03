from django import forms
from django.conf import settings
from . import models
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    SetPasswordForm as BaseSetPasswordForm,
    UserCreationForm as BaseUserCreationForm
)
from django.utils.translation import ugettext_lazy as _

class AuthenticationForm(BaseAuthenticationForm):
    """A subclassed AuthenticationForm that renames `username` to `email`."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"] = self.fields["username"]
        self.fields["email"].widget.attrs = {'class': "form-control", 'placeholder': "you@example.com"}
        self.fields["password"].widget.attrs={'class': "form-control", 'placeholder': "Your password"}
        del self.fields["username"]
        self.fields.move_to_end("password")

    def clean(self):
        self.cleaned_data["username"] = self.cleaned_data["email"]
        cleaned_data = super().clean()
        del cleaned_data["username"]
        return cleaned_data

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        # if not user.email_confirmed:
        #     raise forms.ValidationError(
        #         _("You need to confirm your email address first. "
        #           "Check your email for instructions. "
        #           "If you have not received them, please request a password recovery and we'll send you a new email.")
        #     )


class UserCreationForm(BaseUserCreationForm):
    """A subclassed UserCreationForm that uses `email` instead of `username`."""

    class Meta:
        model = models.User
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(attrs={'class': "form-control", 'placeholder': "you@example.com"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs={'class': "form-control", 'placeholder': "Password"}
        self.fields["password2"].widget.attrs={'class': "form-control", 'placeholder': "Password"}

    def clean_email(self):
        data = self.cleaned_data["email"].lower()
        if models.User.objects.filter(email__iexact=data).exists():
            raise forms.ValidationError(_("This email address is already registered."))
        if not settings.VALIDATE_EMAILS:
            return data
        is_valid, reason = validate_email(data)
        if not is_valid:
            raise forms.ValidationError(reason)
        return data

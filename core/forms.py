from django import forms
from django.conf import settings

from . import models, utils


class NewsSubscriptionForm(forms.ModelForm):

    class Meta:
        model = models.NewsSubscription
        fields = ("email", )

    def clean_email(self):
        data = self.cleaned_data["email"].lower()
        if not settings.VALIDATE_EMAILS:
            return data
        is_valid, reason = utils.validate_email(data)
        if not is_valid:
            raise forms.ValidationError(reason)
        return data

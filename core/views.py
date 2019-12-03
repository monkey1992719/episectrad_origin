from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.generic.edit import BaseFormView

import structlog

from . import forms, models, utils


logger = structlog.getLogger()


class NewsSubscriptionView(BaseFormView):
    form_class = forms.NewsSubscriptionForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed("Method not allowed")

    def render_to_response(self, context):
        if context["form"].errors:
            data = {"success": False, "errors": context["form"].errors.as_json()}
        else:
            data = {"success": True}
            data.update(context["instance"].as_json())
        return JsonResponse(data)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        instance = models.NewsSubscription.objects.filter(email__iexact=email).first()
        if not instance:
            instance = form.save()
            try:
                utils.add_email_to_mailchimp(email)
            except Exception as e:
                logger.bind(email=email, error=repr(e)).exception("Exception adding to Mailchimp")
        return self.render_to_response(self.get_context_data(form=form, instance=instance))

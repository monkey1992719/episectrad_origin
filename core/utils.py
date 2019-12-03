from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _

import requests

import structlog

logger = structlog.get_logger()


def validate_email(address, mailbox_verification=None):
    if not address:
        return False, _("Please enter a valid email address")
    if any(domain in address.casefold() for domain in settings.BLOCKED_EMAIL_DOMAINS):
        domain = address.rsplit("@", 1)[-1]
        return False, _(
            "We have issues sending emails to {domain} based emails. "
            "They get blocked. "
            "Please use another email service like Yahoo or private domain email."
        ).format(domain=domain)
    params = {
        "address": address,
        "api_key": settings.MAILGUN_PUBLIC_API_KEY,
    }
    if mailbox_verification is None:
        mailbox_verification = settings.VALIDATE_EMAILS_MAILBOXES
    if mailbox_verification:
        params["mailbox_verification"] = "true"
    resp = requests.get("https://api.mailgun.net/v2/address/validate", params=params)
    if resp.status_code != 200:
        logger.bind(status=resp.status_code, response=resp.text)\
            .error("Mailgun API error during email validation")
        return True, ""
    data = resp.json()
    is_valid = data.get("is_valid", False)
    suggestion = data.get("did_you_mean", "")
    if not is_valid:
        info = _("Please enter a valid email address")
    elif data.get("is_disposable_address", False):
        is_valid = False
        info = _("Please don't use disposable email services. We won't be able to reach to you.")
    elif data.get("mailbox_verification", None) == "false":  # Note, it's "false", not False
        # Possible values for mailbox_verification are "true", "false", "unknown" and None.
        # For simplicity's sake let's treat anything but "false" (known-invalid) as acceptable here.
        is_valid = False
        info = _("Please enter a valid email address")
    elif suggestion:
        is_valid = True
        info = _("Did you mean {suggestion}?").format(suggestion=suggestion)
    else:
        is_valid = True
        info = ""
    return is_valid, info


def send_template_email(email,
                        from_email,
                        subject_template_name,
                        email_template_name,
                        html_email_template_name,
                        context,
                        lang="en"):
    translation.activate(lang)
    subject = render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [email])
    if html_email_template_name is not None:
        html_email = render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")
    return email_message.send()


# def add_email_to_mailchimp(address):
#     if not all((settings.MAILCHIMP_API_KEY, settings.MAILCHIMP_API_KEY, settings.MAILCHIMP_DC)):
#         logger.bind(email=address).warning("Maichimp settings are not complete")
#         return
#     url = f"https://{settings.MAILCHIMP_DC}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}/members/"
#     res = requests.post(url,
#                         json={"email_address": address, "status": "subscribed"},
#                         auth=("dummyuser", settings.MAILCHIMP_API_KEY))
#     if res.status_code >= 400:
#         logger.bind(email=address, url=url, response=res.text).error("Cant add address to Mailchimp")
#     else:
#         logger.bind(email=address).info("Address was added to Mailchimp")


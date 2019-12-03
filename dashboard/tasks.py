from celery import shared_task

from episectrad import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import structlog

from core.utils import send_template_email

from . import models


logger = structlog.get_logger()

@shared_task
def add(x, y):
    return x + y

@shared_task
def send_signup_email(user_pk, from_email=None,
                      subject_template_name="dashboard/email/signup_subject.txt",
                      email_template_name="dashboard/email/signup_email.txt",
                      html_email_template_name="dashboard/email/signup_email.html",
                      extra_email_context=None):

    logger.bind(extra_email_context=extra_email_context).info("Called send signup email")

    from_email = "ok.star@outlook.com"
    user = models.User.objects.filter(pk=user_pk).first()
    if not user:
        logger.bind(user_pk=user_pk).warning("Unable to find user")
        return
    token_generator = default_token_generator
    context = {
        "email": user.email,
        "uid": user.pk,
        # "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        "token": token_generator.make_token(user),
        "contact_email": settings.CONTACT_EMAIL
    }
    if extra_email_context is not None:
        context.update(extra_email_context)
    logger.bind(email=user.email).info("Sending signup email")
    return send_template_email(user.email, from_email, subject_template_name,
                               email_template_name, html_email_template_name, context)


@shared_task
def send_signup_confirmed_email(user_pk, from_email=None,
                                subject_template_name="dashboard/email/signup_confirmed_email_subject.txt",
                                email_template_name="dashboard/email/signup_confirmed_email.txt",
                                html_email_template_name="dashboard/email/signup_confirmed_email.html",
                                extra_email_context=None):
    user = models.User.objects.filter(pk=user_pk).first()
    if not user:
        logger.bind(user_pk=user_pk).warning("Unable to find user")
        return
    context = {
        "email": user.email,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        "contact_email": settings.CONTACT_EMAIL
    }
    if extra_email_context is not None:
        context.update(extra_email_context)
    logger.bind(email=user.email).info("Sending signup confirmed email")
    return send_template_email(user.email, from_email, subject_template_name,
                               email_template_name, html_email_template_name, context)


@shared_task
def send_email_confirm_email(user_pk, is_new_signup=False, from_email=None,
                             subject_template_name="dashboard/email/password_reset_subject.txt",
                             email_template_name="dashboard/email/password_reset_email.txt",
                             html_email_template_name="dashboard/email/password_reset_email.html",
                             extra_email_context=None):
    user = models.User.objects.filter(pk=user_pk).first()
    if not user:
        logger.bind(user_pk=user_pk).warning("Unable to find user")
        return
    token_generator = default_token_generator
    context = {
        "email": user.email,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        "token": token_generator.make_token(user),
        "is_new_signup": is_new_signup,
        "contact_email": settings.CONTACT_EMAIL
    }
    if extra_email_context is not None:
        context.update(extra_email_context)
    logger.bind(email=user.email).info("Sending password reset email")
    return send_template_email(user.email, from_email, subject_template_name,
                               email_template_name, html_email_template_name, context)


@shared_task
def sync_with_payments_service():
    for item in models.GovernanceItem.objects.exclude(wallet=""):
        item.sync_with_payments_service()
    for item in models.HodlItem.objects.exclude(is_hidden=True):
        item.sync_with_payments_service()

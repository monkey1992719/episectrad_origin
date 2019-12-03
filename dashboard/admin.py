from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _
from hijack_admin.admin import HijackUserAdminMixin

from . import models

@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin, HijackUserAdminMixin):
    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        (_("Permissions"), {
            "fields": (
                "is_active", "is_staff", "is_superuser", "cheater",
                "groups", "user_permissions"
            )
        }),
        (_("Important dates"), {
            "fields": ("last_login", "date_joined")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    ordering = ("email", )
    search_fields = ("email", )
    list_display = (
        "email", "is_staff", "date_joined", "hijack_field"
    )
    change_list_template = "hijack_admin/change_list_user.html"

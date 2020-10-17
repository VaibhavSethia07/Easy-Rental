from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields":
                (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "email_verified",
                    "email_secret",
                )
            },
        ),
    )

    list_display = ("username", "first_name","last_name","is_active", "email", "language","currency", "superhost", "is_staff","is_superuser",)

    list_filter = UserAdmin.list_filter+ ("superhost",)

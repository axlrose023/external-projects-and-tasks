# region				-----External Imports-----
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

# endregion

# region				-----Internal Imports-----
from . import managers

# endregion

# region			  -----Supporting Variables-----
# endregion


class User(AbstractUser):
    # region              -----Information-----
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=150,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name=_("Email address"),
        unique=True,
    )

    email_verified = models.BooleanField(
        verbose_name=_("Email verified"),
        default=True,
    )

    registered_using_social_media = models.BooleanField(
        verbose_name=_("Registered using social media"),
        default=False,
    )
    # endregion

    # region			  -----Supporting Variables-----
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = managers.UserCaseInsensitiveEmailManager()
    # endregion

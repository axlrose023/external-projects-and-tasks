from django.contrib.auth import models as django_auth_models
from django.db import models as django_models


class CaseInsensitiveEmailManager(django_models.Manager):
    def filter(self, *args, **kwargs):
        if "email" in kwargs:
            kwargs["email__iexact"] = kwargs.pop("email")

        email_queries = django_models.Q()

        if "email__in" in kwargs:
            emails = kwargs.pop("email__in")

            for email in emails:
                email_queries |= django_models.Q(email__iexact=email)

        return super().filter(email_queries, *args, **kwargs)


class UserCaseInsensitiveEmailManager(
    django_auth_models.UserManager,
    CaseInsensitiveEmailManager,
):
    def get_by_natural_key(self, username: str):
        filter_field = f"{self.model.USERNAME_FIELD}__iexact"
        return self.get(**{filter_field: username})

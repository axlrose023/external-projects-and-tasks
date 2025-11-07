# region				-----External Imports-----
from django.db import models
from django.utils.translation import gettext_lazy as _
# endregion

# region				-----Internal Imports-----
# endregion

# region			  -----Supporting Variables-----
# endregion


class TimeStampedModel(
    models.Model
):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """
    created_at = models.DateTimeField(
        verbose_name=_(
            "Created date"
        ),
        auto_now_add=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_(
            "Updated date"
        ),
        auto_now=True,
    )

    class Meta:
        abstract = True

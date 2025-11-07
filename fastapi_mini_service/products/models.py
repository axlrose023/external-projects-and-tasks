# region				-----External Imports-----
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import TimeStampedModel
# endregion

# region				-----Internal Imports-----
# endregion

# region			  -----Supporting Variables-----
# endregion

# region				-----Product Models-----
class Product(
    TimeStampedModel
):
    name = models.CharField(
        max_length=255,
        verbose_name=_(
            "Product name"
        ),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_(
            "Description"
        ),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Price"
        ),
    )
    external_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_(
            "External ID"
        ),
        blank=True,
        null=True
    )

    class Meta:
        db_table = "products"
        verbose_name = _(
            "Product"
        )
        verbose_name_plural = _(
            "Products"
        )

    def __str__(
            self
    ):
        if self.external_id:
            return f"{self.name} (External ID: {self.external_id})"
        return self.name
# endregion

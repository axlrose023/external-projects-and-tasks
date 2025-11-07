# region				-----External Imports-----
from django.db import models
# endregion

# region				-----Internal Imports-----
# endregion

# region			  -----Supporting Variables-----
# endregion

# region				-----Models-----
class User(models.Model):
    ext_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=64, blank=True)
    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.ext_id})"


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    building_number = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f"{self.city}, {self.street} {self.building_number}"


class CreditCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="credit_card")
    cc_number = models.CharField(max_length=32)
    cc_type = models.CharField(max_length=32)
    exp_date = models.DateField()

    def __str__(self) -> str:
        return self.cc_number
# endregion

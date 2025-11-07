# region				-----External Imports-----
from django.contrib import admin
from django.db import models
# endregion

# region				-----Internal Imports-----
from .models import Product
# endregion

# region			  -----Supporting Variables-----
# endregion

admin.site.register(Product)
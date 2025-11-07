# region				-----External Imports-----
from django.contrib import admin
# endregion

# region				-----Internal Imports-----
from .models import User
# endregion

# region			  -----Supporting Variables-----
# endregion

admin.site.register(User)
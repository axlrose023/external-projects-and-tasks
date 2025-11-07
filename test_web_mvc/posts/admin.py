# region				-----External Imports-----
from django.contrib import admin
# endregion

# region				-----Internal Imports-----
from .models import Post
# endregion

# region			  -----Supporting Variables-----
# endregion

admin.site.register(Post)
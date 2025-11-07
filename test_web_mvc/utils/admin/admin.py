# region				-----External Imports-----
from django.contrib import admin as django_admin
from unfold import admin as unfold_admin
from django.contrib.sites import models as django_sites_models
from django.contrib.auth import models as django_auth_models
from django.contrib.auth.admin import GroupAdmin

# endregion

# region				-----Internal Imports-----
# endregion


django_admin.site.unregister(django_sites_models.Site)
django_admin.site.unregister(django_auth_models.Group)


@django_admin.register(django_auth_models.Group)
class GroupsAdmin(unfold_admin.ModelAdmin, GroupAdmin): ...

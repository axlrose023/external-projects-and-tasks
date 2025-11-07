from django.contrib import admin

from proxy.models import UserStatistics, UserSite

admin.site.register(UserStatistics)
admin.site.register(UserSite)
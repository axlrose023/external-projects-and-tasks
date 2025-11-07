from django.db import models

from accounts.models import CustomUser


class UserSite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()
    def get_internal_url(self):
        return f'/localhost/{self.name}/'

    def __str__(self):
        return f'{self.user}, {self.url}'


class UserStatistics(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    site = models.ForeignKey(UserSite, on_delete=models.CASCADE, blank=True, null=True)
    page_transitions = models.IntegerField(default=0)
    data_sent = models.BigIntegerField(default=0)
    data_received = models.BigIntegerField(default=0)

    def __str__(self):
        return self.user.username

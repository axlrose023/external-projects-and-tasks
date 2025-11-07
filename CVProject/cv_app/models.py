from django.db import models

class CV(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)
    projects = models.JSONField(default=list, blank=True)
    contacts = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

from django.db import models

from django.db import models


class Office(models.Model):
    cabinet = models.CharField("Кабінет №", max_length=10, unique=True)
    description = models.TextField("Опис")

    def __str__(self):
        return f"Office {self.cabinet}"


class Person(models.Model):
    office = models.ForeignKey(Office, related_name="persons", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    rank = models.CharField("Звання", max_length=50)

    def __str__(self):
        return f"{self.name} - {self.rank} - {self.position}"

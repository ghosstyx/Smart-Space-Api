from django.db import models
from accounts.models import NaturalPerson


class MarkTrack(models.Model):
    arrival = models.TimeField(auto_now=False, auto_now_add=False, null=True, verbose_name="Время прихода персоны")
    person = models.ForeignKey(NaturalPerson, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.arrival}  : Время на работе"

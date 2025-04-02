from django.db import models
from accounts.models import NaturalPerson


class MarkTrack(models.Model):
    checkTime = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, verbose_name="Время прихода персоны")
    checkType = models.CharField(max_length=255, verbose_name="IN or OUT")
    person = models.ForeignKey(NaturalPerson, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.checkTime}  : Время на работе"

class BioTrack(models.Model):
    ip_address = models.CharField(max_length=255, verbose_name="IP Address")
    port = models.IntegerField(verbose_name="Port")
    title = models.CharField(max_length=255, verbose_name="Title")
    password = models.CharField(default=1,max_length=255, verbose_name="Password")
    class Meta:
        verbose_name = "Био Трек"
        verbose_name_plural = "Био Треки"


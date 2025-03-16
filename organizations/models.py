from django.db import models
from accounts.models import *

class Organization(models.Model):
    organizationTitle = models.CharField(max_length=255, verbose_name="Название организации")
    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.organizationTitle


class Branch(models.Model):
    branchTitle = models.CharField(max_length=255, verbose_name="Название филиала")
    organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return self.branchTitle





class Department(models.Model):
    departmentTitle = models.CharField(max_length=255, verbose_name="Название Подразделения")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True,)
    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return self.departmentTitle



class JobTitle(models.Model):
    jobTitle = models.CharField(max_length=255, verbose_name="Название должности")
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.jobTitle



class BioTrack(models.Model):
    ip_address = models.CharField(max_length=255, verbose_name="IP Address")
    port = models.IntegerField(verbose_name="Port")
    title = models.CharField(max_length=255, verbose_name="Title")
    password = models.CharField(max_length=255, verbose_name="Password")
    class Meta:
        verbose_name = "Био Трек"
        verbose_name_plural = "Био Треки"


class WorkHours(models.Model):
    arrive = models.TimeField(auto_now=False, auto_now_add=False, null=True, verbose_name="Время прихода")
    leave = models.TimeField(auto_now=False, auto_now_add=False, null=True, verbose_name="Время Ухода")
    def __str__(self):
        return f"{self.arrive} - {self.leave}"
    class Meta:
        verbose_name = "Часы Работы"
        verbose_name_plural = "Часы Работы"


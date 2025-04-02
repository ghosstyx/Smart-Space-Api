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
    deptName = models.CharField(max_length=255, verbose_name="Название Подразделения")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True,)
    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return self.deptName
class JobTitle(models.Model):
    jobTitle = models.CharField(max_length=255, verbose_name="Название должности")
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
    def __str__(self):
        return self.jobTitle
class WorkHours(models.Model):
    schName = models.CharField(max_length=255, verbose_name="Название филиала")
    StartTime = models.DateTimeField(auto_now=False, auto_now_add=False, default=None, null=True, verbose_name="Время прихода")
    EndTime = models.DateTimeField(auto_now=False, auto_now_add=False, default=None, null=True, verbose_name="Время Ухода")
    def __str__(self):
        return f"{self.StartTime} - {self.EndTime}"
    class Meta:
        verbose_name = "Часы Работы"
        verbose_name_plural = "Часы Работы"


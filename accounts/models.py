from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from accounts.managers import UserManager
from organizations.models import *

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, verbose_name='Электронная почта')
    phone_number = PhoneNumberField(unique=True, verbose_name='Номер телефона')
    middle_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Отчество')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

class NaturalPerson(models.Model):
    pnf = models.IntegerField(unique=True, verbose_name="ПИНФЛ")
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="ФИО")
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    jobTitle = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    work_hours = models.ForeignKey(WorkHours, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Люди"
    def __str__(self):
        return f"{self.full_name} {self.birthday}"


class LogSms(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    phone_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Номер телефона')
    message = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сообщение')
    resp = models.CharField(max_length=800, null=True, blank=True, verbose_name='Ответ')

    class Meta:
        verbose_name = 'SMS Log'
        verbose_name_plural = 'SMS Logs'

    def __str__(self):
        return f"{self.phone_number} | {self.message}"


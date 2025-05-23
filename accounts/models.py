from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import NaturalPersonManager
from organizations.models import *

class NaturalPerson(AbstractUser):
    username = None
    pnf = models.IntegerField(default=12345, blank=True, null=True, verbose_name="ПИНФЛ")
    phone = models.CharField(max_length=13, unique=True, verbose_name="Номер телефона")
    about = models.TextField(max_length=1000, blank=True, null=True, verbose_name="О себе")
    is_department_head = models.BooleanField(default=False)

    # Организационные поля
    branch = models.ForeignKey(Branch, blank=True, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    jobTitle = models.ForeignKey(JobTitle, blank=True, null=True, on_delete=models.SET_NULL)
    work_hours = models.ForeignKey(WorkHours, blank=True, null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = NaturalPersonManager()

    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Люди"

    def __str__(self):
        return f"{self.get_full_name() or self.email}"

    def get_active_chats(self):
        return self.chats.all()

    def get_absolute_url(self):
        return reverse('user_profiles:profile', kwargs={'pk': self.id})


class LogSms(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Номер телефона')
    message = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сообщение')
    resp = models.CharField(max_length=800, null=True, blank=True, verbose_name='Ответ')

    class Meta:
        verbose_name = 'SMS Log'
        verbose_name_plural = 'SMS Logs'

    def __str__(self):
        return f"{self.phone_number} | {self.message}"


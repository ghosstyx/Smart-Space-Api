from django.db import models
from accounts.models import NaturalPerson
from django.utils import timezone

class Chat(models.Model):
    participants = models.ManyToManyField(NaturalPerson, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-last_message']

    def __str__(self):
        return f"Чат между: {', '.join([str(p) for p in self.participants.all()])}"

    def update_last_message(self):
        self.last_message = timezone.now()
        self.save()

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.chat.update_last_message()

    def __str__(self):
        return f"{self.sender} в {self.timestamp.strftime('%H:%M')}: {self.text[:30]}"
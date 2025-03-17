from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(MarkTrack)
class MarkTrackAdmin(admin.ModelAdmin):
    list_display = ('arrival', 'person',)

@admin.register(BioTrack)
class BioTrackAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "port", "title", "password")

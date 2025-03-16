from django.contrib import admin
from .models import *

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("branchTitle","organization",)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("organizationTitle",)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("departmentTitle", "organization", )

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("jobTitle", )


@admin.register(BioTrack)
class BioTrackAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "port", "title", "password")

@admin.register(WorkHours)
class WorkHoursAdmin(admin.ModelAdmin):
    list_display = ("arrive", "leave",)

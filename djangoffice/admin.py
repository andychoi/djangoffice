from django.contrib import admin

from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass
@admin.register(ArtifactType)
class ArtifactTypeAdmin(admin.ModelAdmin):
    pass
@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    pass
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass
@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    pass
@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(SQLReport)
class SQLReportAdmin(admin.ModelAdmin):
    pass
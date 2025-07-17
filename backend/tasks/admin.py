# Register your models here.
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'status', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('priority', 'status', 'due_date')

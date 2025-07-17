# tasks/admin.py
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_users', 'priority', 'status', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('priority', 'status', 'due_date')

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    get_users.short_description = 'Usuarios'

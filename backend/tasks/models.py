from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta')
    ])
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=[
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completada')
    ])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    shared_with = models.ManyToManyField(User, related_name='shared_tasks', blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

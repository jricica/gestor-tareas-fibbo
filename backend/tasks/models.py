from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta')])
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pendiente'), ('in_progress', 'En progreso'), ('completed', 'Completada')])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # 👈 Asegúrate de que sea 'user', no 'users'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

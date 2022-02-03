from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Task(models.Model):
    STATUS_CHOICES = [
        ('ToDo', 'ToDo'),
        ('In Progres', 'In Progres'),
        ('Done', 'Done'),
        ('Close', 'Close'),
    ]
    task_name = models.CharField(max_length=30)
    task_description = models.TextField(max_length=300)
    coment = models.CharField(max_length=30, default='Sin comentarios')
    expiration_day = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default='ToDo', choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    task_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.titulo


    def __str__(self):
        return f'{self.task_name.title()}'

    @property
    def is_past_due(self):
        return datetime.today() > self.expiration_day.replace(tzinfo=None)

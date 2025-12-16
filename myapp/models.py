from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class User(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)
    mobileNo = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50,default='staff')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} ({self.email})"

class Task(models.Model):
    taskid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    taslDetails = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.taskid}"
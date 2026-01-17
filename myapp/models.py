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
    
class Work(models.Model):
    workid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    workAssignedTo = models.ForeignKey(User, on_delete=models.CASCADE)
    workTask = models.ForeignKey(Task, on_delete=models.CASCADE)
    workDescription = models.TextField(blank=True)
    assignedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Work assigned to {self.workAssignedTo.username} for task {self.workTask.taskid}"
    
class SalesAndExpenses(models.Model):
    salesid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    salesData = models.JSONField(default=dict)

    def __str__(self):
        return f"Total Income: {self.salesData.get('total_income', 0)} and Total Expenses: {self.salesData.get('total_outgoing', 0)}"
    

class RMA(models.Model):
    rmaid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rmaDetails = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"RMA Data: {self.rmaDetails}"
    
class Attendance(models.Model):
    attendanceid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attendanceDetails = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Attendance Data: {self.attendanceDetails}"
from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.student_id} - {self.user}"

from django.db import models
from project.models import Project
from student.models import Student
from django.contrib.auth.models import User


class ThesisApply(models.Model):
    thesis_apply_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    applied_students = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, default='Pending')
    cv = models.FileField(upload_to='cv/', blank=True)

    def __str__(self):
        return f"{self.thesis_apply_id} - {self.project}"

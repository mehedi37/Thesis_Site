from django.db import models
from project.models import Project
from student.models import Student
from django.contrib.auth.models import User


class ThesisApply(models.Model):
    thesis_apply_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    applied_student = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, default='Pending')
    terms_accepted = models.BooleanField(default=False)
    cv = models.FileField(upload_to='cv/', blank=True)
    supervisor_approval = models.BooleanField(default=False)
    supervisor_checked = models.BooleanField(default=False)
    unit_co_checked = models.BooleanField(default=False)
    unit_co_approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.thesis_apply_id} - {self.project}"

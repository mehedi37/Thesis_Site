from django.db import models
from project.models import Project
from student.models import Student


class ThesisApply(models.Model):
    thesis_apply_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    applied_students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return f"{self.thesis_apply_id} - {self.project}"

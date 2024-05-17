from django.db import models
from supervisor.models import Supervisor
from unit_co.models import UnitCoordinator
from student.models import Student


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    project_detail = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    max_students = models.IntegerField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    unit_coordinator = models.ForeignKey(
        UnitCoordinator, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return f"{self.project_id}_{self.name}_{self.supervisor.user.username}"

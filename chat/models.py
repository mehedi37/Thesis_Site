from django.db import models
from django.contrib.auth.models import User, Group
from supervisor.models import Supervisor
from unit_co.models import UnitCoordinator

# Create your models here.

class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    conversation_title = models.CharField(max_length=255)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    unit_co = models.ForeignKey(UnitCoordinator, on_delete=models.CASCADE, null=True)
    read_users = models.ManyToManyField(User, related_name='read_users', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation_id} - {self.group} | {self.timestamp}"

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user}"

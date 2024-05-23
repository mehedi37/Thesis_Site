# Generated by Django 5.0.6 on 2024-05-23 04:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_conversation_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='read_users',
            field=models.ManyToManyField(blank=True, related_name='read_users', to=settings.AUTH_USER_MODEL),
        ),
    ]

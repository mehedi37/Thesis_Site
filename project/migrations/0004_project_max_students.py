# Generated by Django 5.0.6 on 2024-05-17 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_project_project_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='max_students',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

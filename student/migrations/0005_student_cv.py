# Generated by Django 5.0.6 on 2024-05-21 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_student_group_delete_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cv',
            field=models.FileField(null=True, upload_to='cv/'),
        ),
    ]

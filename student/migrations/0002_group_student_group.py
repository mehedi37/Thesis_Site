# Generated by Django 5.0.6 on 2024-05-21 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=255)),
                ('group_password', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.group'),
        ),
    ]

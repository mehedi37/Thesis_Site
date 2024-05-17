# Generated by Django 5.0.6 on 2024-05-17 22:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesis_apply', '0003_thesisapply_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesisapply',
            name='applied_students',
        ),
        migrations.AddField(
            model_name='thesisapply',
            name='applied_students',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-16 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unit_co', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitcoordinator',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-21 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thesis_apply', '0011_thesisapply_unit_co_approval'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesisapply',
            name='unit_co_approval',
        ),
        migrations.RemoveField(
            model_name='thesisapply',
            name='unit_co_checked',
        ),
    ]

# Generated by Django 4.0.8 on 2023-09-17 10:56

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_alter_event_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_id',
            field=models.CharField(default=events.models.generate_unique_team_id, max_length=12, unique=True),
        ),
    ]
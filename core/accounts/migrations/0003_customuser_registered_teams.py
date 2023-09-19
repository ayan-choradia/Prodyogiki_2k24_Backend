# Generated by Django 4.0.8 on 2023-09-16 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_team_registered_users'),
        ('accounts', '0002_customuser_registered_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='registered_teams',
            field=models.ManyToManyField(blank=True, related_name='reg_users_teams', to='events.team'),
        ),
    ]
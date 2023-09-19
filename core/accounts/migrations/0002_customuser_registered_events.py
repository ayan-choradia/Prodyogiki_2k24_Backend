# Generated by Django 4.0.8 on 2023-09-15 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_registered_users'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='registered_events',
            field=models.ManyToManyField(blank=True, related_name='reg_users', to='events.event'),
        ),
    ]
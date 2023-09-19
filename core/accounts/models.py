from django.contrib.auth.models import AbstractUser
from django.db import models
import random


def generate_default_user_id():
    return f'#PY{random.randint(100000000, 999999999)}'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_id = models.CharField(
        max_length=12, unique=True, default=generate_default_user_id)
    registered_events = models.ManyToManyField(
        'events.Event', related_name='reg_users', blank=True)
    registered_teams = models.ManyToManyField(
        'events.Team', related_name='reg_users_teams', blank=True)

    def __str__(self):
        return f'{self.username} - {self.user_id}'

    def register_for_event(self, event):
        self.registered_events.add(event)

    def register_for_team(self, team):
        self.registered_teams.add(team)

    def clear_registered_events(self):
        for event in self.registered_events.all():
            event.registered_users.remove(self)

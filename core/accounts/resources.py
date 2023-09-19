from import_export import resources, fields
from .models import CustomUser


class RegisteredEventsField(fields.Field):
    def export(self, obj):
        return ", ".join([event.name for event in obj.registered_events.all()])


class RegisteredTeamsField(fields.Field):
    def export(self, obj):
        return ", ".join([team.name for team in obj.registered_teams.all()])


class CustomUserResource(resources.ModelResource):
    username = fields.Field(attribute='username')
    email = fields.Field(attribute='email')
    user_id = fields.Field(attribute='user_id')
    registered_events = RegisteredEventsField(
        column_name='registered_events', attribute='registered_events')
    registered_teams = RegisteredTeamsField(
        column_name='registered_teams', attribute='registered_teams')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_id',
                  'registered_events', 'registered_teams')

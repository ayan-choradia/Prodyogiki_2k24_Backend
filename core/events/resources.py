from import_export import resources, fields
from .models import Team, Event


class RegisteredEventsField(fields.Field):
    def export(self, obj):
        return ", ".join([event.name for event in obj.registered_events.all()])


class RegisteredTeamsField(fields.Field):
    def export(self, obj):
        return ", ".join([team.name for team in obj.registered_teams.all()])


class RegisteredUsersField(fields.Field):
    def export(self, obj):
        users_with_id = [
            f"{user.username}({user.user_id})" for user in obj.registered_users.all()]
        return ", ".join(users_with_id)


class CustomTeamResource(resources.ModelResource):
    name = fields.Field(attribute='name')
    team_id = fields.Field(attribute='team_id')
    registered_events = RegisteredEventsField(
        column_name='registered_events', attribute='registered_events')
    registered_users = RegisteredUsersField(
        column_name='registered_users', attribute='registered_users')

    class Meta:
        model = Team
        fields = ('name', 'team_id',
                  'registered_events', 'registered_users')


class CustomEventResource(resources.ModelResource):
    name = fields.Field(attribute='name')
    registered_teams = RegisteredTeamsField(
        column_name='registered_teams', attribute='registered_teams')
    registered_users = RegisteredUsersField(
        column_name='registered_users', attribute='registered_users')

    class Meta:
        model = Event
        fields = ('name',
                  'registered_teams', 'registered_users')

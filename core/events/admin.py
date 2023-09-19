from django.contrib import admin
from .models import Event, Team
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import RelatedFieldListFilter
from .resources import CustomTeamResource, CustomEventResource


class CustomRelatedFieldListFilter(RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        return field.get_choices(include_blank=False)


class EventAdmin(ImportExportModelAdmin):
    resource_class = CustomEventResource
    list_display = ('id', 'name', 'get_registered_users',
                    'get_registered_teams')
    list_filter = [('registered_users', CustomRelatedFieldListFilter),
                   ('registered_teams', CustomRelatedFieldListFilter)]
    search_fields = ['name', 'description',
                     'registered_users__username', 'registered_teams__name']

    def get_registered_users(self, obj):
        return ", ".join([user.username for user in obj.registered_users.all()])

    def get_registered_teams(self, obj):
        return ", ".join([team.name for team in obj.registered_teams.all()])

    get_registered_users.short_description = 'Registered Users'
    get_registered_teams.short_description = 'Registered Teams'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return []
        # Creating a new object
        return ['registered_users', 'registered_teams']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if change:
            updated_registered_users = set(
                form.instance.registered_users.all())

            removed_users = set(
                form.initial['registered_users']) - updated_registered_users

            added_users = updated_registered_users - \
                set(form.initial['registered_users'])

            for user in removed_users:
                user.registered_events.remove(form.instance)

            for user in added_users:
                user.registered_events.add(form.instance)

            updated_registered_teams = set(
                form.instance.registered_teams.all())
            removed_teams = set(
                form.initial['registered_teams']) - updated_registered_teams
            added_teams = updated_registered_teams - \
                set(form.initial['registered_teams'])

            for team in removed_teams:
                team.registered_events.remove(form.instance)

            for team in added_teams:
                team.registered_events.add(form.instance)


class TeamAdmin(ImportExportModelAdmin):
    resource_class = CustomTeamResource
    list_display = ('id', 'name', 'team_id',
                    'get_registered_users', 'get_registered_events')
    # list_filter = ('registered_events__name',)
    # search_fields = ['name', 'registered_events']
    list_filter = [('registered_events', CustomRelatedFieldListFilter),
                   ('registered_users', CustomRelatedFieldListFilter)]
    search_fields = ['name', 'registered_events__name',]

    def get_registered_users(self, obj):
        return ", ".join([user.username for user in obj.registered_users.all()])

    get_registered_users.short_description = 'Registered Users'

    def get_registered_events(self, obj):
        return ", ".join([event.name for event in obj.registered_events.all()])

    get_registered_events.short_description = 'Registered Events'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return []
        return ['registered_users', 'registered_events']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if change:
            updated_registered_users = set(
                form.instance.registered_users.all())
            print(" updated users", updated_registered_users)
            removed_users = set(
                form.initial['registered_users']) - updated_registered_users

            added_users = updated_registered_users - \
                set(form.initial['registered_users'])
            print(f"added_users {added_users}")
            for user in removed_users:
                user.registered_teams.remove(form.instance)

            for user in added_users:
                user.registered_teams.add(form.instance)

            updated_registered_events = set(
                form.instance.registered_events.all())
            removed_events = set(
                form.initial['registered_events']) - updated_registered_events

            added_events = updated_registered_events - \
                set(form.initial['registered_events'])
            for event in removed_events:
                event.registered_teams.remove(form.instance)

            for event in added_events:
                event.registered_teams.add(form.instance)


admin.site.register(Event, EventAdmin)
admin.site.register(Team, TeamAdmin)

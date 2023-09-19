from django.contrib import admin
from .models import CustomUser
from import_export.admin import ImportExportModelAdmin
from .resources import CustomUserResource
from django.contrib.admin import RelatedFieldListFilter


class CustomRelatedFieldListFilter(RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        return field.get_choices(include_blank=False)


class CustomUserAdmin(ImportExportModelAdmin):
    resource_class = CustomUserResource
    list_display = ('username', 'email', 'user_id',
                    'get_registered_events', 'get_registered_teams')

    list_filter = [('registered_events', CustomRelatedFieldListFilter),
                   ('registered_teams', CustomRelatedFieldListFilter)]
    search_fields = ['name', 'registered_events__name',
                     'registered_teams__name']

    def get_registered_events(self, obj):
        return ", ".join([event.name for event in obj.registered_events.all()])

    get_registered_events.short_description = 'Registered Events'

    def get_registered_teams(self, obj):
        return ", ".join([team.name for team in obj.registered_teams.all()])

    get_registered_teams.short_description = 'Registered Teams'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return []
        return ['registered_teams', 'registered_events']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # Get the updated set of registered events after saving
        updated_registered_events = set(form.instance.registered_events.all())

        # Find events that were removed from registration
        removed_events = set(
            form.initial['registered_events']) - updated_registered_events

        # Find events that were added to registration
        added_events = updated_registered_events - \
            set(form.initial['registered_events'])

        # Remove user from removed events' registered_users
        for event in removed_events:
            event.registered_users.remove(form.instance)

        # Add user to added events' registered_users
        for event in added_events:
            event.registered_users.add(form.instance)

        # Get the updated set of registered events after saving
        updated_registered_teams = set(form.instance.registered_teams.all())

        # Find events that were removed from registration
        removed_teams = set(
            form.initial['registered_teams']) - updated_registered_teams

        # Find events that were added to registration
        added_teams = updated_registered_teams - \
            set(form.initial['registered_teams'])

        # Remove user from removed events' registered_users
        for team in removed_teams:
            team.registered_users.remove(form.instance)

        # Add user to added events' registered_users
        for team in added_teams:
            team.registered_users.add(form.instance)


admin.site.register(CustomUser, CustomUserAdmin)

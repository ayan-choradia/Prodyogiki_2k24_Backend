from django.urls import path
# from .views import EventListView, EventDetailView, TeamView, TeamDetailView, register_event, register_team
from .views import EventListView, EventDetailView, create_team, join_team, join_team_event

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    #     path('teams/', TeamView.as_view(), name='team-list'),
    #     path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    #     path('register_event/<int:event_id>/',
    #          register_event, name='register_event'),
    #     path('register_team/<int:team_id>/',
    #          register_team, name='register_team'),
    path('create-team/', create_team, name='create-team'),
    path('join-team/', join_team, name='join-team'),
    path('join-team-event/<int:event_id>/', join_team_event,
         name='join-team-event'),  # Add this line


]

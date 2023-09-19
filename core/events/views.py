from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics
from .models import Event, Team
from .serializers import EventSerializer, EventRegistrationSerializer, TeamSerializer, JoinTeamEventSerializer
from accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# class TeamView(generics.ListCreateAPIView):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer


# class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer


@api_view(['POST'])
def register_event(request, event_id):
    if request.method == 'POST':
        serializer = EventRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            try:
                user = CustomUser.objects.get(user_id=user_id)
                event = Event.objects.get(id=event_id)
                if user.registered_events.filter(id=event_id).exists():
                    return Response({'error': 'User is already registered for this event'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.registered_events.add(event)
                    # Update the registered_users field of the event
                    event.registered_users.add(user)
                    return Response({'message': 'Event registered successfully'}, status=status.HTTP_201_CREATED)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User with provided user_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except Event.DoesNotExist:
                return Response({'error': 'Event with provided event_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @api_view(['POST'])
# def register_team(request, team_id):
#     if request.method == 'POST':
#         serializer = EventRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user_id = serializer.validated_data['user_id']
#             try:
#                 user = CustomUser.objects.get(user_id=user_id)
#                 team = Team.objects.get(id=team_id)
#                 if user.registered_teams.filter(id=team_id).exists():
#                     return Response({'error': 'User is already registered for this event'}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     user.registered_teams.add(team)
#                     # Update the registered_users field of the event
#                     team.registered_users.add(user)
#                     return Response({'message': 'Event registered successfully'}, status=status.HTTP_201_CREATED)
#             except CustomUser.DoesNotExist:
#                 return Response({'error': 'User with provided user_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
#             except Team.DoesNotExist:
#                 return Response({'error': 'Event with provided event_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def create_team(request):
    if request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'team_id': serializer.data['team_id']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def join_team(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        team_id = request.data.get('team_id')

        try:
            team = Team.objects.get(team_id=team_id)
            user = CustomUser.objects.get(user_id=user_id)
            if user not in team.registered_users.all():
                team.registered_users.add(user)
                user.registered_teams.add(team)
                return Response({'message': 'User added to the team successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User is already a member of this team.'}, status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            return Response({'message': 'Team does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def join_team_event(request, event_id):
    if request.method == 'POST':
        team_id = request.data.get('team_id')

        try:
            event = Event.objects.get(pk=event_id)
            team = Team.objects.get(team_id=team_id)

            # Register team for the event
            event.registered_teams.add(team)
            team.registered_events.add(event)

            # Transfer registered users to event
            event.registered_users.add(*team.registered_users.all())
            for user in team.registered_users.all():
                user.registered_events.add(event)

            return Response({'message': 'Team successfully registered for event.'}, status=status.HTTP_200_OK)

        except Event.DoesNotExist:
            return Response({'message': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Team.DoesNotExist:
            return Response({'message': 'Team does not exist.'}, status=status.HTTP_404_NOT_FOUND)

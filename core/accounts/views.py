from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import HttpResponse
import csv
import json
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from rest_framework.authtoken.models import Token
from .tasks import test_func


def test_func_celery(request):
    test_func.delay()
    return HttpResponse("Done")


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # After the user is created, you can add the user_id to the response data
        # Assuming the user_id is returned by the serializer
        print(response.data)
        user_id = response.data.get('user_id')
        if user_id is not None:
            response.data['user_id'] = user_id

        return Response({'Prodyogiki ID': user_id}, status=status.HTTP_200_OK)


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAuthenticated])
class UserLogoutView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

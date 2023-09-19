# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser
import random


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        # Generate unique user ID
        user_id = self.generate_unique_user_id()
        user.user_id = user_id
        user.save()

        return user

    def generate_unique_user_id(self):
        user_id = f'#PY{random.randint(100000000, 999999999)}'
        while CustomUser.objects.filter(user_id=user_id).exists():
            user_id = f'#PY{random.randint(100000000, 999999999)}'
        return user_id

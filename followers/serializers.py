from rest_framework import serializers
from django.db import IntegrityError
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle the conversion of the follower model instances
    into JSON and back.

    Contains a Meta class to provide further information to
    itself.

    Contains a create method to handle cases when a user tries to follow a user
    they are already following

    """
    user = serializers.ReadOnlyField(source='user.username')
    followed_user_name = serializers.ReadOnlyField(
        source='followed_user.username'
    )

    class Meta:
        model = Follower
        fields = [
            'id', 'user', 'followed_user', 'created_date', 'followed_user_name'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
             'detail': ('You are already following this user')
            })

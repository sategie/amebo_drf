from rest_framework import serializers
from django.db import IntegrityError
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle the conversion of the like model instances 
    into JSON and back.

    Contains a Meta class to provide further information to 
    itself.

    Contains a create method to handle cases when a user tries to like a post
    more than once

    """

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_date']


    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'You have already liked this post'
            })
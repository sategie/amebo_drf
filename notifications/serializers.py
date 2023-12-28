from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle the conversion of the notification model instances 
    into JSON and back.

    Contains a Meta class to provide further information to 
    itself.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'message', 'created_date', 'seen'
        ]
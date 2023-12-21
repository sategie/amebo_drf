from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle the conversion of the profile model instances into
    JSON and back.
    """
    class Meta:
        model = Profile
        fields = ['user', 'name', 'created_date', 'image']
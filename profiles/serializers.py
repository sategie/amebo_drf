from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle the conversion of the profile model instances 
    into JSON and back.

    Contains an own_profile field and method for authentication purposes

    Contains a Meta class to provide further information to 
    itself
    """
    user = serializers.ReadOnlyField(source='user.username')
    own_profile = serializers.SerializerMethodField()

    def get_own_profile(self, obj):
        """
        Method which defines how the own_profile field is derived.

        Takes an obj parameter which refers to the Profile model instance
        
        Checks if the serialized profile belongs to the currently logged in
        user making the request
        """
        request = self.context['request']
        return request.user == obj.user

    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'created_date', 'image', 'own_profile']
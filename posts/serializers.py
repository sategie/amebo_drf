from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle the conversion of the post model instances 
    into JSON and back.

    Contains an own_post field and method for authentication purposes

    Contains a Meta class to provide further information to 
    itself
    """
    user = serializers.ReadOnlyField(source='user.username')
    own_post = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='user.profile.id')
    profile_image = serializers.ReadOnlyField(source='user.profile.image.url')

    def get_own_post(self, obj):
        request = self.context['request']
        return request.user == obj.user

    class Meta:
        model = Post
        fields = ['id', 'user','own_post', 'profile_id', 'profile_image', 'title', 'post_content', 'image', 'created_date', 'updated_date']

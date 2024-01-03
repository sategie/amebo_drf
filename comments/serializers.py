from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle the conversion of the comment model instances 
    into JSON and back.

    Contains an own_comment field and method for authentication purposes.

    Contains a Meta class to provide further information to 
    itself.

    """
    user = serializers.ReadOnlyField(source='user.username')
    own_comment = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='user.profile.id')
    profile_image = serializers.ReadOnlyField(source='user.profile.image.url')
    post_title = serializers.CharField(read_only=True, source='post.title')

    def get_own_comment(self, obj):
        request = self.context['request']
        return request.user == obj.user

    class Meta:
        model = Comment
        fields = ['id', 'user', 'own_comment', 'profile_id', 'profile_image', 'post', 'comment_content', 'created_date', 'updated_date', 'post_title']


from rest_framework import serializers
from .models import Post
from comments.models import Comment
from likes.models import Like
from followers.models import Follower


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle the conversion of the post model instances
    into JSON and back.

    Contains an own_post field and method for authentication purposes

    Contains a Meta class to provide further information to itself
    """
    user = serializers.ReadOnlyField(source='user.username')
    own_post = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='user.profile.id')
    profile_image = serializers.ReadOnlyField(source='user.profile.image.url')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()

    def get_own_post(self, obj):
        request = self.context['request']
        return request.user == obj.user

    def get_comments_count(self, obj):
        """
        Returns the total number of comments on the post
        """
        return Comment.objects.filter(post=obj).count()

    def get_likes_count(self, obj):
        """
        Returns the total number of likes on the post
        """
        return Like.objects.filter(post=obj).count()

    def get_follower_count(self, obj):
        """
        Returns the total number of followers of the user who created the post
        """
        return Follower.objects.filter(followed_user=obj.user).count()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'own_post', 'profile_id', 'profile_image',
            'title', 'post_content', 'image', 'created_date', 'updated_date',
            'comments_count', 'likes_count', 'follower_count'
        ]

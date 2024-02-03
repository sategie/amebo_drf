from rest_framework import serializers
from .models import Profile
from posts.models import Post
from followers.models import Follower


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
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_own_profile(self, obj):
        """
        Method which defines how the own_profile field is derived.

        Takes an obj parameter which refers to the Profile model instance

        Checks if the serialized profile belongs to the currently logged in
        user making the request
        """
        request = self.context['request']
        return request.user == obj.user

    def get_posts_count(self, obj):
        return Post.objects.filter(user=obj.user).count()

    def get_following_id(self, obj):
        request = self.context['request']
        user = request.user
        if user.is_authenticated:
            following = Follower.objects.filter(
                user=user, followed_user=obj.user
            ).first()
            print(following)
            return following.id if following else None
        return None

    def get_followers_count(self, obj):
        return Follower.objects.filter(followed_user=obj.user).count()

    def get_following_count(self, obj):
        return obj.user.following.count()

    class Meta:
        model = Profile
        fields = [
         'id', 'user', 'name', 'created_date', 'image',
         'own_profile', 'posts_count', 'following_id', 'followers_count',
         'following_count'
        ]

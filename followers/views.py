from rest_framework import status, permissions, generics, serializers, filters
from .models import Follower
from .serializers import FollowerSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class FollowerList(generics.ListCreateAPIView):
    """
    View which handles the listing of all follower objects and creation of a
    new follower
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer    
    filter_backends = [
     filters.OrderingFilter,
     filters.SearchFilter,
     DjangoFilterBackend
]
    search_fields = ['user__username', 'followed_user__username', 'created_date']
    filterset_fields = ['user__username', 'followed_user']

    def get_queryset(self):
        """
        Fetches all followers associated with the logged in user.
        """
        user_following_ids = self.request.user.following.values_list('followed_user', flat=True)
        return Follower.objects.filter(followed_user__in=user_following_ids)
            
        

    def perform_create(self, serializer):
        """
        Prevent user from following themselves and save the follower to the database if valid.
        """
        if serializer.validated_data.get('followed_user') == self.request.user:
            raise serializers.ValidationError({'detail': 'You cannot follow yourself.'})
        serializer.save(user=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    View which handles the listing and deleting of a single follower object
    """
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Only allow users to access their own follower details
        """
        return self.queryset.filter(user=self.request.user)
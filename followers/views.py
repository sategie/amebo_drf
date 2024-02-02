from rest_framework import status, permissions, generics, serializers, filters
from .models import Follower
from .serializers import FollowerSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class FollowerList(generics.ListCreateAPIView):
    """
    View which handles the listing of all followed user
    objects and creation of a new follower
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    filter_backends = [
     filters.OrderingFilter,
     filters.SearchFilter,
     DjangoFilterBackend
    ]
    search_fields = [
     'user__username',
     'followed_user',
     'created_date'
    ]

    filterset_fields = ['user__username', 'followed_user']

    def perform_create(self, serializer):
         serializer.save(user=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    View which handles the listing and deleting of a single follower object
    """
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsOwnerOrReadOnly]

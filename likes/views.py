from rest_framework import status, permissions, generics, filters
from .models import Like
from .serializers import LikeSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class LikeList(generics.ListCreateAPIView):
    """
    View which lists all likes or creates a new like
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    filter_backends = [
     filters.OrderingFilter,
     filters.SearchFilter,
     DjangoFilterBackend
    ]
    search_fields = ['user__username', 'post__title', 'created_date']
    filterset_fields = ['user__username', 'post']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    View which lists a single like or deletes a single like
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()

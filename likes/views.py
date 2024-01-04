from rest_framework import status, permissions, generics
from django.http import Http404
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class LikeList(generics.ListCreateAPIView):
    """
    View which lists all likes or creates a new like
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

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
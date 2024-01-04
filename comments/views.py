from rest_framework import generics, permissions, filters
from django.http import Http404
from .models import Comment
from .serializers import CommentSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class CommentList(generics.ListCreateAPIView):
    """
    View which handles the listing of all comments and creation of a new comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
     filters.OrderingFilter,
     filters.SearchFilter,
     DjangoFilterBackend
]
    search_fields = ['user__username', 'created_date', 'post__title']
    filterset_fields = ['user__username', 'post']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View which handles getting, updating and deleting a single comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
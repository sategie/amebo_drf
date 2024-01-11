from rest_framework import generics, permissions, filters
from .models import Post
from followers.models import Follower
from .serializers import PostSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError


class PostList(generics.ListCreateAPIView):
    """
    View which handles the listing and creation of new post objects
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
     filters.OrderingFilter,
     filters.SearchFilter,
     DjangoFilterBackend
]
    search_fields = ['title', 'user__username', 'created_date']
    filterset_fields = ['title', 'user__username']


    def perform_create(self, serializer):
        """
        Check if a post with the same title already exists (case insenstive).

        Display a message informing that the user already has an existing post
        with the same title.

        Create a new post instance if it is not a duplicate title.
        """
        title = serializer.validated_data['title'].lower()
        if Post.objects.filter(title__iexact=title, user=self.request.user).exists():
            raise ValidationError("You already have an existing post with this title")
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View which handles the API requests for a single post object
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
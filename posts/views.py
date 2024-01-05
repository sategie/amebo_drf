from rest_framework import generics, permissions, filters
from .models import Post
from followers.models import Follower
from .serializers import PostSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class PostList(generics.ListCreateAPIView):
    """
    View which handles the listing and creation of new post objects
    """
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    filter_backends = [
     filters.OrderingFilter,
     filters.SearchFilter,
     DjangoFilterBackend
]
    search_fields = ['title', 'user__username', 'created_date']
    filterset_fields = ['title', 'user__username']

    def get_queryset(self):
        """
        Returns a list of all posts
        for the currently authenticated user.
        """
        followed_users = Follower.objects.filter(user=self.request.user).values_list('followed_user', flat=True)
        followed_users = list(followed_users) + [self.request.user.id]
        return Post.objects.filter(user__in=followed_users)

    def perform_create(self, serializer):
        """
        Create a new post instance.
        """
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View which handles the API requests for a single post object
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
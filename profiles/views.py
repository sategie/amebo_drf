from rest_framework import generics, permissions, filters
from .models import Profile
from .serializers import ProfileSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class ProfileList(generics.ListAPIView):
    """
    View which handles the listing of all profile objects
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
     filters.OrderingFilter,
     DjangoFilterBackend
]
filterset_fields = ['user__username', 'created_date']


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    View which handles the listing and updating of a single profile object
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes =[IsOwnerOrReadOnly]


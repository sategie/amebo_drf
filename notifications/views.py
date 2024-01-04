from rest_framework import status, permissions, generics
from django.http import Http404
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class NotificationList(generics.ListAPIView):
    """
    View which handles the listing of all notifications
    and creation of a new notification.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Fetches all notifications associated with the logged in user.
        Marks the notifications as 'seen' using the update method.
        Return the queryset.
        """
        queryset = Notification.objects.filter(user=self.request.user)
        queryset.update(seen=True)
        return queryset

class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View which handles the retrieving, updating and deleting of a notification
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Retrieves a queryset with notifications for the logged in user.
        """
        return Notification.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        """
        Updates the seen attribute of the notification to True.
        """
        serializer.save(seen=True)
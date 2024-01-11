from rest_framework import status, permissions, generics, filters
from .models import Notification
from .serializers import NotificationSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class NotificationList(generics.ListAPIView):
    """
    View which handles the listing of all notifications
    and creation of a new notification.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
     filters.OrderingFilter,
     filters.SearchFilter,
     DjangoFilterBackend
]
    search_fields = ['message', 'user__username', 'created_date']
    filterset_fields = ['seen', 'user__username']

    def get_queryset(self):
        """
        Fetches all notifications associated with the logged in user.
        Marks the notifications as 'seen' using the update method.
        Return the queryset.
        """
        queryset = Notification.objects.filter(user=self.request.user)
        queryset.update(seen=True)
        return queryset

class NotificationDetail(generics.RetrieveDestroyAPIView):
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

    # def perform_update(self, serializer):
    #     """
    #     Updates the seen attribute of the notification to True.
    #     """
    #     serializer.save(seen=True)
from rest_framework import status, permissions, generics, filters
from rest_framework.response import Response
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
        """
        return Notification.objects.filter(user=self.request.user)


class NotificationDetail(generics.RetrieveDestroyAPIView):
    """
    View which handles retrieving and deleting a notification
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Retrieves a queryset with notifications for the logged in user.
        """
        return Notification.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Marks the notification as seen only when it is retrieved in the detail
        view.
        """
        instance = self.get_object()
        instance.seen = True
        instance.save(update_fields=['seen'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

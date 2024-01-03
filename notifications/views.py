# from rest_framework import status, permissions
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Notification
# from .serializers import NotificationSerializer
# from amebo_drf.permissions import IsOwnerOrReadOnly

# class NotificationList(APIView):
#     """
#     View which handles the listing and creation of new notifications
#     """

#     serializer_class = NotificationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         """
#         Fetches all notifications associated with the logged in user.

#         Marks the notifications as 'seen' using the update method.

#         Return the serialized data.
#         """
#         notifications = Notification.objects.filter(user=request.user)
#         serializer = NotificationSerializer(notifications, many=True)
#         notifications.update(seen=True)
        
#         return Response(serializer.data)


# class NotificationDetail(APIView):
#     """
#     View which handles the retrieval, updating and deleting of a notification
#     """
#     serializer_class = NotificationSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#     def get_object(self, pk):
#         """
#         Retrieves a notification object from the database.

#         Raises an error if the notification does not exist

#         """
#         try:
#             notification = Notification.objects.get(pk=pk, user=self.request.user)
#             self.check_object_permissions(self.request, notification)
#             return notification
#         except Notification.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         """
#         Calls the get_object method to get the valid notification from the database.

#         Updates the seen attribute of the notification to True.

#         Saves the updated notification to the database.

#         Serializes the notification.

#         Returns the serialized data to the client as JSON.
#         """
#         notification = self.get_object(pk)
#         notification.seen = True
#         notification.save(update_fields=['seen'])
        
#         serializer = NotificationSerializer(notification)
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         """
#         Handles a DELETE request to the API for a particular notification.

#         Retrieves the notification instance and deletes it.

#         Returns a response showing that the notification has been deleted

#         """
#         notification = self.get_object(pk)
#         notification.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import status, permissions, generics
from django.http import Http404
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class NotificationList(generics.ListAPIView):
    """
    View which handles the listing and creation of new notifications
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
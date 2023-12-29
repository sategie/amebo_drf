from rest_framework import status, permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Follower
from .serializers import FollowerSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class FollowerList(APIView):
    """
    View which handles the listing and creation of new follower objects
    """
    serializer_class = FollowerSerializer    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Fetches all followers associated with the logged in user.
        
        Returns the serialized data.        
        """
        user_following_ids = request.user.following.values_list('followed_user', flat=True)
        followers = Follower.objects.filter(followed_user__in=user_following_ids)

        serializer = FollowerSerializer(followers, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """
        Gets a serialized follower instance.

        Saves the follower to the database if valid.

        Returns a HTTP 201 created message if valid.

        Returns a HTTP 400 bad request message if invalid.
        """
        serializer = FollowerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Prevent user from following themselves
             if serializer.validated_data.get('followed_user') == request.user:
                return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
             serializer.save(user=request.user)
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowerDetail(APIView):
    """
    View which handles the API requests for a single follower object

    """
    serializer_class = FollowerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        """
        Retrieves a follower object from the database.

        Raises an error if the follower does not exist

        """
        try:
            follower = Follower.objects.get(pk=pk)
            self.check_object_permissions(self.request, follower)
            return follower
        except Follower.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Handles a GET request to the API for a particular follower.

        Retrieves the follower instance and serializes this into JSON.

        Returns a response with the serialized follower data

        """
        follower = self.get_object(pk)
        serializer = FollowerSerializer(follower, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Handles a DELETE request to the API for a particular follower.

        Retrieves the follower instance and deletes it.

        Returns a response showing that the follower has been deleted

        """
        follower = self.get_object(pk)
        follower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

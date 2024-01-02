from rest_framework import status, permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class LikeList(APIView):
    """
    View which handles the listing and creation of new like objects
    """
    serializer_class = LikeSerializer    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Fetches all likes.

        Returns the serialized data.
        """
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """
        Gets a serialized like instance.

        Saves the like to the database if valid.

        Returns a HTTP 201 created message if valid.

        Returns a HTTP 400 bad request message if invalid.
        """
        serializer = LikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeDetail(APIView):
    """
    View which handles the API requests for a single like object

    """
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        """
        Retrieves a like object from the database.

        Raises an error if the like does not exist
        """
        try:
            like = Like.objects.get(pk=pk)
            self.check_object_permissions(self.request, like)
            return like
        except Like.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Handles a GET request to the API for a particular like.

        Retrieves the like instance and serializes this into JSON.

        Returns a response with the serialized like data

        """
        like = self.get_object(pk)
        serializer = LikeSerializer(like, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Handles a DELETE request to the API for a particular like.

        Retrieves the like instance and deletes it.

        Returns a response showing that the like has been deleted

        """
        like = self.get_object(pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

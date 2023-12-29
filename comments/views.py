from rest_framework import status, permissions
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class CommentList(APIView):
    """
    View which handles the listing and creation of new comment objects
    """
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        """
        Fetches all comments

        Returns the serialized data
        """
        comments = Comment.objects.all()
        serializer = CommentSerializer(
            comments, many = True, context = {'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(
            data=request.data, context ={'request': request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

class CommentDetail(APIView):
    """
    View which handles the API requests for a single comment object
    """
    serializer_class = CommentSerializer
    permission_classes =[IsOwnerOrReadOnly]


    def get_object(self, pk):
        """
        Retrieves a comment object from the database.
        Raises an error if the particular comment does not exist
        """
        try:
            comment=Comment.objects.get(pk=pk)
            self.check_object_permissions(self.request, comment)
            return comment
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Handles a GET request to the API for a particular comment.
        Retrieves the comment instance and serializes this into JSON.
        Returns a response with the serialized comment data
        """
        comment = self.get_object(pk)
        serializer=CommentSerializer(comment, context= {'request' : request})
        return Response(serializer.data)

    def put (self, request, pk):
        """
        Handles a PUT request to the API for a particular comment.
        
        """
        comment =self.get_object(pk)
        serializer=CommentSerializer(comment, data=request.data, context= {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles a DELETE request to the API for a particular comment.
        Retrieves the comment instance and deletes it.
        Returns a response showing that the comment has been deleted
        """
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from followers.models import Follower
from .serializers import PostSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class PostList(APIView):
    """
    View which handles the listing and creation of new post objects
    """
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        """
        Fetches the ids of the users that are being followed by the current user.

        Include the current user's id in the list of users to fetch posts from.

        Fetches the posts and filters them to include only those that belong to
        followed users and the current user.

        Returns the serialized data
        """

        followed_users = Follower.objects.filter(user=request.user).values_list('followed_user', flat=True)
        followed_users = list(followed_users) + [request.user.id]
        posts = Post.objects.filter(user__in=followed_users)
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)


    def post(self, request):
        """
        Gets a serialized post instance.

        Saves the post to the database if valid.

        Returns a HTTP 201 created message if valid.

        Returns a HTTP 400 bad request message if invalid.
        """
        serializer = PostSerializer(
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

class PostDetail(APIView):
    """
    View which handles the API requests for a single post object
    """
    serializer_class = PostSerializer
    permission_classes =[IsOwnerOrReadOnly]


    def get_object(self, pk):
        """
        Retrieves a post object from the database.
        Raises an error if the particular post does not exist
        """
        try:
            post=Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Handles a GET request to the API for a particular post.
        Retrieves the post instance and serializes this into JSON.
        Returns a response with the serialized post data
        """
        post = self.get_object(pk)
        serializer=PostSerializer(post, context= {'request' : request})
        return Response(serializer.data)

    def put (self, request, pk):
        """
        Handles a PUT request to the API for a particular post.
        
        """
        post =self.get_object(pk)
        serializer=PostSerializer(post, data=request.data, context= {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles a DELETE request to the API for a particular post.
        Retrieves the post instance and deletes it.
        Returns a response showing that the post has been deleted
        """
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
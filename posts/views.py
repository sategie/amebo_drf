from rest_framework import status, permissions
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class PostList(APIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many = True, context = {'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
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
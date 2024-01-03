# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Profile
# from .serializers import ProfileSerializer
# from django.http import Http404
# from rest_framework import status, permissions
# from amebo_drf.permissions import IsOwnerOrReadOnly


# class ProfileList(APIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     """
#     View which handles the listing of new profile objects
#     """
#     def get(self, request):
#         """
#         Fetches all profiles.

#         Returns the serialized data.
#         """
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(profiles, many= True, context= {'request' : request})
#         return Response(serializer.data)


# class ProfileDetail(APIView):
#     """
#     View which handles the API requests for a single profile object
#     """
#     serializer_class = ProfileSerializer
#     permission_classes =[IsOwnerOrReadOnly]


#     def get_object(self, pk):
#         """
#         Retrieves a profile object from the database.
#         Raises an error if the particular profile does not exist
#         """
#         try:
#             profile=Profile.objects.get(pk=pk)
#             self.check_object_permissions(self.request, profile)
#             return profile
#         except Profile.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         """
#         Handles a GET request to the API for a particular profile.
#         Retrieves the profile instance and serializes this into JSON.
#         Returns a response with the serialized profile data
#         """
#         profile = self.get_object(pk)
#         serializer=ProfileSerializer(profile, context= {'request' : request})
#         return Response(serializer.data)

#     def put (self, request, pk):
#         """
#         Handles a PUT request to the API for a particular profile.
        
#         """
#         profile =self.get_object(pk)
#         serializer=ProfileSerializer(profile, data=request.data, context= {'request' : request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from amebo_drf.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListAPIView):
    """
    View which handles the listing of all profile objects
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    View which handles the listing and updating of a single profile object
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes =[IsOwnerOrReadOnly]


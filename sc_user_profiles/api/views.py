from django.shortcuts import render
from api.custom_exceptions import CustomApiException
import django_filters
from rest_framework import filters
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.http import JsonResponse
from django.http import HttpResponse
from api.serializers import UserSerializer, ProfileSerializer
from api.authorization import IsNonAdminUser, IsAdminUser 
from rest_framework import status
from api.models import User, Profile, UserArchive
from api.signals import manipulate_user_profile
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404, get_list_or_404


# Create your views here.
@api_view(['POST'])
def create_user(request):
    """
    A create user view
    if is_admin is true two profiles Admin and Officer are created
    else only Officer profile is created.
    """
    try:        
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"data":user_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": settings.INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserList(generics.ListAPIView):
    """
    A simple ViewSet for listing users
    Only non admin and active users can perform this action.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsNonAdminUser,)



# @api_view(['GET'])
# def list_users(request):
#   try:    
#       #only non admin users should access this api
#       #add pagination
#       users = User.objects.all()
#       users_serializer = UserSerializer(users, many=True)
#       return Response({"data":users_serializer.data}) 
#   except Exception as e:
#       return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_profiles(request, user_id):
    """
    A list user profiles by user_id view.
    """
    try:  
        user = get_object_or_404(User, pk = user_id)
        profiles = get_list_or_404(Profile, user = user)
        profiles_serializer = ProfileSerializer(profiles, many=True)
        return Response({"data":profiles_serializer.data})  
    except Exception as e:
      return Response({"message": settings.INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['DELETE'])
@permission_classes((IsAdminUser, ))
def delete_user(request, user_id):
    """
    A delete user by user_id view.
    Currently it is hard delete, we can make it soft delete
    by setting is_active flag to false and moving record to archive 
    """
    user = get_object_or_404(User, pk = user_id)
    UserArchive.objects.create(name = user.name, username = user.username, email= user.email, 
                token= user.token, is_active= False, is_admin= user.is_admin, created= user.created, last_updated= user.last_updated)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)  
    

@api_view(['PUT'])
@permission_classes((IsAdminUser, ))
def updateUserDetails(request, user_id):
    """
    Update user details view
    depending on is_admin flag, admin profile is either created or deleted.
    """
    user = get_object_or_404(User, pk = user_id)      
    user_serializer = UserSerializer(user, data = request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        post_save.connect(manipulate_user_profile, sender=User)
        return Response({"data":user_serializer.data}, status=status.HTTP_200_OK)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.shortcuts import render
from api.custom_exceptions import CustomApiException
import django_filters
from rest_framework import filters
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse
from api.serializers import UserSerializer, ProfileSerializer
# from api.services import SearchService 
from rest_framework import status
from api.models import User, Profile
from django.shortcuts import get_object_or_404, get_list_or_404


# Create your views here.
@api_view(['POST'])
def create_user(request):
	try:		
		user_serializer = UserSerializer(data = request.data)
		if user_serializer.is_valid():
			user_serializer.save()
			return Response({"data":user_serializer.data}, status=status.HTTP_201_CREATED)
		return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_users(request):
	try:	
		#add pagination
		users = User.objects.all()
		users_serializer = UserSerializer(users, many=True)
		return Response({"data":users_serializer.data})	
	except Exception as e:
		return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_profiles(request, user_id):
	# try:	
		user = get_object_or_404(User, pk = user_id)
		profiles = get_list_or_404(Profile, user = user)
		profiles_serializer = ProfileSerializer(profiles, many=True)
		return Response({"data":profiles_serializer.data})	
	# except Exception as e:
	# 	print(e)
	# 	return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		# HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		# return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})
# @csrf_exempt
def home(request):
	"""
	request contains q param with one or more characters
	returns: list of matched city names limited to 50 results
	"""
	return Response({'message': 'HOME'})
	# try:
	# 	search_query = request.GET.get('q', '').strip()
	# 	if not search_query:
	# 		raise CustomApiException("Please provide atleast one character to search city by name", status.HTTP_400_BAD_REQUEST)

	# 	search_service = SearchService()
	# 	result = search_service.search_city_by_name(search_query)

	# 	HttpResponse.status_code = status.HTTP_200_OK
	# 	return JsonResponse(result, safe=False)
	# except CustomApiException as err:
	# 	HttpResponse.status_code = err.status_code
	# 	return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	# except Exception, e:
	# 	HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
	# 	return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})

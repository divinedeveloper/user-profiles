from rest_framework import permissions
from django.conf import settings
from rest_framework import status
from api.models import User
from django.shortcuts import get_object_or_404
from api.custom_exceptions import CustomApiException
import jwt


def decode_token_user(request):
	token = request.META.get('HTTP_TOKEN')
	if token:
		try:
			decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
			user = get_object_or_404(User, token = token)
			return (user, decoded_token)			
		except (jwt.ExpiredSignatureError, jwt.DecodeError) as e:
			raise CustomApiException("Invalid Token", status.HTTP_403_FORBIDDEN)
	else:
		return False


class IsNonAdminUser(permissions.BasePermission):
	"""
	Permission to check if user is not admin.
	"""
	def has_permission(self, request, view):
		#get JWT token from request
		#decode it and check is_admin and is_active flags
		#if admin false and active true then return true else false
		(user, decoded_token) = decode_token_user(request)
		if not user.is_admin and user.is_active:
			return True
		else:
			raise CustomApiException("Only active non admin users are allowed to perform this action", status.HTTP_403_FORBIDDEN)

		# token = request.META.get('HTTP_TOKEN')
		# if token:
		# 	try:
		# 		decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
		# 		user = get_object_or_404(User, token = token)
				
		# 	except (jwt.ExpiredSignatureError, jwt.DecodeError) as e:
		# 		raise CustomApiException("Invalid Token", status.HTTP_403_FORBIDDEN)
		# else:
		# 	return False

class IsAdminUser(permissions.BasePermission):
	"""
	Permission to check if user is admin or owner of entity.
	"""
	def has_permission(self, request, view):
		#get JWT token from request
		#decode it and check is_admin and is_active flags
		#if admin false and active true then return true else false
		(user, decoded_token) = decode_token_user(request)
		if user.is_admin:
			return True
		else:
			raise CustomApiException("Only admin can execute this action.", status.HTTP_403_FORBIDDEN)

        
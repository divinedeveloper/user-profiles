from rest_framework import serializers
from api.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
	"""
	User serializer for user records
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = User
		fields = ('id', 'name', 'username', 'email', 'token', 'is_admin', 'created', 'last_updated')
		depth = 3

class ProfileSerializer(serializers.ModelSerializer):
	"""
	Profile serializer for profile records
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = Profile
		fields = ('id', 'name', 'created')
		depth = 3
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from api.models import User, Profile
from django.db.models import Max
from django.conf import settings
import jwt


@receiver(pre_save, sender = User)
def create_user_token(sender, instance, **kwargs):
	token = jwt.encode({'is_admin': instance.is_admin, 'is_active': instance.is_active}, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
	instance.token = token.decode('ascii')


@receiver(post_save, sender = User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
    	Profile.objects.create(user = instance, name = 'Officer')
    	if instance.is_admin:
    		Profile.objects.create(user = instance, name = 'Admin')


# @receiver(post_save, sender = User)
def manipulate_user_profile(sender, instance, **kwargs):
	#check if user admin profile exists
	#if admin is set create profile if doesnt exists else delete it
	try:
		admin_profile = Profile.objects.get(user = instance, name = 'Admin')
		if not instance.is_admin and admin_profile:
			admin_profile.delete()
	except Profile.DoesNotExist as e:
		if instance.is_admin:
			Profile.objects.create(user = instance, name = 'Admin')



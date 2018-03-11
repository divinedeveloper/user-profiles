from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from api.models import User, Profile
from django.db.models import Max
from django.conf import settings
import jwt


@receiver(pre_save, sender = User)
def create_user_token(sender, instance, **kwargs):
    # id__max is None if there are no Users in the database
	id_max = User.objects.all().aggregate(Max('id'))['id__max']
	id_next = id_max + 1 if id_max else 1
	instance.token = jwt.encode({'is_admin': instance.is_admin, 'is_active': instance.is_active, 'user_id' : id_next}, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


@receiver(post_save, sender = User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
    	Profile.objects.create(user = instance, name = 'Officer')
    	if instance.is_admin:
    		Profile.objects.create(user = instance, name = 'Admin')


# @receiver(post_save, sender = User)
def manipulate_user_profile(sender, instance, **kwargs):
	#check if user admin profile exists
	admin_profile = Profile.objects.get(user = instance, name = 'Admin')

	if instance.is_admin:
		#if not exists create one
		if not admin_profile:
			Profile.objects.create(user = instance, name = 'Admin')
	else:
		#delete if it exists
		if admin_profile:
			admin_profile.delete()
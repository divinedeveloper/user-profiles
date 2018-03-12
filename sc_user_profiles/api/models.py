from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
	"""
	User model with fields
	Default ordering is descending by created field.
	"""
	name = models.CharField(blank = True, max_length = 30)
	username = models.CharField(blank = False, max_length = 150, unique = True)
	email = models.EmailField(blank = False, max_length = 254, unique = True)
	token = models.CharField(blank = True, max_length = 100)
	is_active = models.BooleanField(default = True)
	is_admin = models.BooleanField(default = True)
	created = models.DateTimeField(default = timezone.now)
	last_updated = models.DateTimeField(default = timezone.now)

	class Meta:
		ordering = ('-created',)


class Profile(models.Model):
	"""
	Profile model with fields
	Only Admin and Officer types allowed.
	"""
	PROFILE_TYPE = (
        ('OFFICER', 'Officer'),
        ('ADMIN', 'Admin'),
    )

	name = models.CharField(max_length = 7, blank = False, choices = PROFILE_TYPE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	created = models.DateTimeField(default = timezone.now)

class UserArchive(models.Model):
	"""
	User Archive model for soft delete
	User data is removed from User table and moved into this table for future reference
	"""
	name = models.CharField(blank = True, max_length = 30)
	username = models.CharField(blank = False, max_length = 150)
	email = models.EmailField(blank = False, max_length = 254)
	token = models.CharField(blank = True, max_length = 100)
	is_active = models.BooleanField(default = False)
	is_admin = models.BooleanField(default = True)
	created = models.DateTimeField()
	last_updated = models.DateTimeField()
	deleted_on = models.DateTimeField(default = timezone.now)



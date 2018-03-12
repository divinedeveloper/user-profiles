from django.apps import AppConfig
from django.db.models.signals import post_save
# from api.signals import manipulate_user_profile


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = 'api'

    def ready(self):
    	from api.models import User, Profile
    	import api.signals  # noqa
    	from api.signals import manipulate_user_profile
    	post_save.connect(manipulate_user_profile, sender=User)
"""sc_user_profiles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('addUser', views.create_user, name='create_user'),
    path('listUsers', views.list_users, name='list_users'),
    path('deleteUser', views.home, name='home'),
    path('updateUserDetails', views.home, name='home'),
    path('listProfiles/<int:user_id>', views.list_profiles, name='list_profiles'),
]

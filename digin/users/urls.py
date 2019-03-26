# users/urls.py
from django.urls import include, path

from . import views
import rest_framework.authtoken.views as token_view
from django.contrib.auth import views as auth_views
app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
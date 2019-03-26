from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework import generics
from rest_framework.decorators import authentication_classes, permission_classes

from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import connection
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy



def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))
              for row in cursor.fetchall()]

# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]
from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# @permission_classes([])
# class UserListView(generic.ListView):
    
#     # queryset = models.CustomUser.objects.all()
#     serializer_class = serializers.UserSerializer
#     model = models.CustomUser
#     template_name = 'users/login.html'
#     form = CustomUserChangeForm()

#     def get_queryset(self):
#         # cursor = connection.cursor()
        
#         # cursor.execute("SELECT * FROM users_customuser")
        
#         # data = dictfetchall(cursor)
#         return models.CustomUser.objects.raw("SELECT * FROM users_customuser")#Response(data, content_type="application/json", status=200)#models.Poll.objects.raw("SELECT * FROM polls_poll WHERE owner_id=%s", [user.id])
    


# @permission_classes([])
# class Logout(APIView):
#     def get(self, request, format=None):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)
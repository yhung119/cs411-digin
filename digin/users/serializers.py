# users/serializers.py
from rest_framework import serializers
from . import models
from django.contrib.auth.hashers import make_password
from django.db import connection


# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     def create(self, validated_data):

#         # user = models.CustomUser.objects.create(**validated_data)
    
#         with connection.cursor() as cursor:
#             cursor.execute("INSERT INTO users_customuser"
#                            "(password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, name)"
#                            "VALUES (%s, 0, %s, '', '', %s, 0, 1, NOW(), %s)",
#                            (make_password(validated_data["password"]), validated_data["username"], validated_data["email"], validated_data["name"])
#             )
#             cursor.execute("SELECT * FROM users_customuser WHERE username=%s", [validated_data["username"]])
            
#             validated_data['id'] = cursor.fetchone()[0] # 0 is default position

#         user = models.CustomUser(**validated_data)
#         return user

#     class Meta:
#         model = models.CustomUser
#         fields = ('password', 'username', 'name', 'email', 'id')


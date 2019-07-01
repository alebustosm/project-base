from django.urls import path, include
from django.contrib.auth.models import Group
from ..models import User, Role
from django.contrib import admin
from rest_framework.response import Response
admin.autodiscover()
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import UserModelSerializer,GroupSerializer,UserSerializer
from django.db import transaction
from rest_framework.permissions import AllowAny


ROLE_TYPE = ['admin','user']

class UserCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('profile') in ROLE_TYPE:
            return super().create(request, *args, **kwargs)
        else:
            return Response({'profile': ['This field accept user or admin .']}, status=400)


    # def create(self, request, *args, **kwargs):
    #     with transaction.atomic():
    #         profile_user = request.data.get('profile', None)
    #         if profile_user:
    #             try:
    #                 user = User()
    #                 user.set_password(request.data.get('password', None))
    #                 user.email = request.data.get('email', None)
    #                 user.save()               
    #                 rol = Role.objects.create(user=user,type=profile_user)
    #                 return Response(UserSerializer(user).data, status=201)
    #             except Exception as e:
    #                 return Response({'user': ['This ID not belong to Professional.']}, status=400)

    




class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

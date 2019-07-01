from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import Group
from ..models import User, Role, ROL_ADMIN, ROL_USER

ROLE_TYPE = ['admin','user']

class UserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data,*args,**kwargs):
        with transaction.atomic():
            request = self.context.get('request',None)
            profile_user = request.data.get('profile',None)
            if profile_user in ROLE_TYPE:
                user = User.objects.create(**validated_data)
                user.set_password(request.data.get('password',None))
                user.save()
                rol = Role.objects.create(user=user,type=profile_user)
                return user
           
    class Meta:
        model = User
        fields = ('username','email', "first_name", "last_name")
    
        

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )

class RoleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        exclude = ('created_at', 'updated_at')

class UserModelSerializer(serializers.ModelSerializer):
    roles = RoleModelSerializer(many=True)

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'groups','is_staff','is_active','user_permissions')



from django.contrib import admin
from .models import User, Role

@admin.register(User, Role)
class UserAdmin(admin.ModelAdmin):
    pass
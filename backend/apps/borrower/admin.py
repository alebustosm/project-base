from django.contrib import admin
from .models import Borrower

@admin.register(Borrower)
class UserAdmin(admin.ModelAdmin):
    pass
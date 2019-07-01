from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .api.api_rest import UserCreate, UserDetails, GroupList



urlpatterns = [
    path('', UserCreate.as_view()),
    path('<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
]

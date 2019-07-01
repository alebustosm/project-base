from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', include('apps.user.urls')),
]

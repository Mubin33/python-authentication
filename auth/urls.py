
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('knox.urls')), 
    path('api/password-reset/', include('django_rest_passwordreset.urls'), name='password-reset'),
]

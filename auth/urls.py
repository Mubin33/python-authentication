
from django.contrib import admin
from django.urls import path, include
from users.views import send_email_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('knox.urls')), 
]

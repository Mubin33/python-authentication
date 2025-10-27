
from django.contrib import admin
from django.urls import path, include 
from knox import views as knox_views 
from users.views import UserProfileView

# for make a api doc
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="My Project API",
      default_version='v1',
      description="API documentation for authentication and user management",
      contact=openapi.Contact(email="you@example.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    
# for make a api doc
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),



# 
    path('admin/', admin.site.urls),
    path('/', include('users.urls')),
    # path('api-auth/', include('rest_framework.urls')),
   #  path('api/auth/', include('knox.urls')), 
    path('api/password-reset/', include('django_rest_passwordreset.urls'), name='password-reset'),
    
    # logout  
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
 
#  get active login user
  path('profile/', UserProfileView.as_view(), name='user-profile'),
]

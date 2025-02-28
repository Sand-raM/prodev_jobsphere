"""
URL configuration for jobsphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import debug_toolbar

# Define the schema view for Swagger documentation
schema_view = get_schema_view(
   openapi.Info(
      title="JobSphere API",
      default_version='v1',
      description="""
      JobSphere API allows users to browse, post, and apply for jobs efficiently.
      
      ### Features:
      - **Users**: Register, login, and apply for jobs.
      - **Jobs**: CRUD operations for job postings.
      - **Applications**: Users can apply for jobs and track their applications.

      **Authentication:**  
      - All endpoints require authentication via JWT tokens.  
      - Use `/api/auth/login/` to obtain a token.  
      - Include `Authorization: Bearer <token>` in headers for protected endpoints.
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="gabrieltuyishimire35@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('job_board.urls')),  # Include job board app URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path("__debug__/", include(debug_toolbar.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplicationViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),  # This includes /jobs/ and /applications/
]

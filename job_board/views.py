from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import Group
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer

# Helper function to check user roles
def user_has_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

# Custom Permissions
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admins can modify job postings. Others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Read access for everyone
        return request.user.is_authenticated and (request.user.is_superuser or user_has_group(request.user, "Admin"))

class IsApplicantOrAdmin(permissions.BasePermission):
    """
    Only applicants can view/edit their own applications. Admins can view all applications.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_superuser or user_has_group(request.user, "Admin")

class JobPagination(PageNumberPagination):
    page_size = 10  # Show 10 jobs per page

class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    pagination_class = JobPagination

# Job ViewSet
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.prefetch_related('applications').all()
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['post'], url_path='apply', permission_classes=[permissions.IsAuthenticated])
    def apply(self, request, pk=None):
        job = self.get_object()
        user = request.user

        cover_letter = request.data.get('cover_letter')
        resume = request.FILES.get('resume')

        if not cover_letter:
            raise ValidationError({"cover_letter": "This field is required."})
        if not resume:
            raise ValidationError({"resume": "This field is required."})

        if Application.objects.filter(job=job, user=user).exists():
            return Response({"error": "You have already applied for this job."}, status=status.HTTP_400_BAD_REQUEST)

        application = Application.objects.create(
            job=job,
            user=user,
            cover_letter=cover_letter,
            resume=resume
        )

        return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)

# Application ViewSet
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsApplicantOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user_has_group(user, "Admin") or user_has_group(user, "Staff"):
            return Application.objects.all()
        return Application.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        application = self.get_object()
        if request.user != application.user and not (request.user.is_superuser or user_has_group(request.user, "Admin")):
            raise PermissionDenied("You do not have permission to delete this application.")
        return super().destroy(request, *args, **kwargs)

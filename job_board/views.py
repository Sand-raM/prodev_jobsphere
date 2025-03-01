# jobsphere/job_board/views.py
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import Group
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer
from .permissions import IsAdminOrReadOnly, IsApplicantOrAdmin

# Helper function to check user roles
def user_has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# Custom Permissions
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admins can modify job postings. Others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Read access for everyone
        return request.user.is_authenticated and user_has_group(request.user, "Admin")  # Only admins can write


class IsApplicantOrAdmin(permissions.BasePermission):
    """
    Only applicants can view/edit their own applications. Admins can view all applications.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or user_has_group(request.user, "Admin")  # Owners & Admins

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
    """
    Job ViewSet handles job postings.

    **Endpoints:**
    - `GET /jobs/` - List all jobs.
    - `POST /jobs/` - Create a new job (Admin only).
    - `GET /jobs/{id}/` - Retrieve job details.
    - `PUT/PATCH /jobs/{id}/` - Update a job (Admin only).
    - `DELETE /jobs/{id}/` - Delete a job (Admin only).
    - `POST /jobs/{id}/apply/` - Apply for a job.

    **Permissions:**
    - Admins can create, update, and delete jobs.
    - Regular users can only view jobs.
    """
    @action(detail=True, methods=['post'], url_path='apply', permission_classes=[permissions.IsAuthenticated])
    def apply(self, request, pk=None):

        """
        Apply for a job.
        
        **Request Body:**
        ```json
        {
            "cover_letter": "I am very interested in this position...",
            "resume": "<file>"
        }
        ```

        **Responses:**
        - `201 Created` - Application submitted successfully.
        - `400 Bad Request` - Missing cover letter or resume.
        - `403 Forbidden` - User has already applied.
        """
        job = self.get_object()
        user = request.user

        # Validate input data
        cover_letter = request.data.get('cover_letter')
        resume = request.FILES.get('resume')

        if not cover_letter:
            raise ValidationError({"cover_letter": "This field is required."})
        if not resume:
            raise ValidationError({"resume": "This field is required."})

        # Prevent duplicate applications
        if Application.objects.filter(job=job, user=user).exists():
            return Response({"error": "You have already applied for this job."}, status=status.HTTP_400_BAD_REQUEST)

        # Create application
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
        if user_has_group(user, "Admin") or user_has_group(user, "Staff"):
            return Application.objects.all()  # Admins & Staff see all applications
        return Application.objects.filter(user=user)  # Users see only their own applications

    def destroy(self, request, *args, **kwargs):
        application = self.get_object()
        if request.user != application.user and not user_has_group(request.user, "Admin"):
            raise PermissionDenied("You do not have permission to delete this application.")
        return super().destroy(request, *args, **kwargs)

# jobsphere/job_board/permissions.py
from rest_framework import permissions

def user_has_group(user, group_name):
    """
    Check if a user belongs to a specific group.
    """
    return user.groups.filter(name=group_name).exists()

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admins can modify job postings (create, update, delete). Others can only read.
    """
    def has_permission(self, request, view):
        # Allow read-only access (GET, HEAD, OPTIONS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow only admins to write (POST, PUT, DELETE)
        return request.user.is_authenticated and user_has_group(request.user, "Admin")

    def has_object_permission(self, request, view, obj):
        """
        Allow admins to perform actions (create, update, delete) on all jobs.
        Users can only access jobs they have posted.
        """
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow anyone to read job postings
        return user_has_group(request.user, "Admin")  # Only admins can modify jobs

class IsApplicantOrAdmin(permissions.BasePermission):
    """
    Only applicants can view/edit their own applications. Admins can view all applications.
    """
    def has_object_permission(self, request, view, obj):
        # Allow applicants to manage their own applications
        if request.user == obj.user:
            return True
        # Allow admins to manage all applications
        return user_has_group(request.user, "Admin")

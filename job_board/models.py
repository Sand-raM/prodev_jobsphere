from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=255, db_index=True)  # Indexed for faster search
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)  # Indexed for filtering
    salary = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # Indexed for filtering
    category = models.CharField(max_length=255, db_index=True)  # Indexed for category-based filtering
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),  # Ensures quick searches by job title
            models.Index(fields=['location']),  # Optimizes location-based filtering
            models.Index(fields=['category']),  # Optimizes category-based filtering
        ]

    def __str__(self):
        return self.title
class Application(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=50, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

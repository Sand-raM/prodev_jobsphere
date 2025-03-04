# jobsphere/job_board/serializers.py
from rest_framework import serializers
from .models import Job, Application

# Serializer for Job model
class JobSerializer(serializers.ModelSerializer):
    """
    Job Serializer - Used for job listings.

    **Example Response:**
    ```json
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Exciting job opportunity...",
        "location": "Remote",
        "salary": "$80,000 - $100,000",
        "category": "Engineering",
        "created_at": "2025-02-26T12:00:00Z",
        "updated_at": "2025-02-26T12:30:00Z"
    }
    ```
    """
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary', 'category', 'created_at', 'updated_at']

# Serializer for Application model
class ApplicationSerializer(serializers.ModelSerializer):

    """
    Application Serializer - Handles job applications.

    **Example Response:**
    ```json
    {
        "id": 10,
        "job": 1,
        "user": 5,
        "cover_letter": "I am excited about this opportunity...",
        "resume": "resume.pdf",
        "status": "Pending",
        "applied_at": "2025-02-26T13:45:00Z"
    }
    ```
    """

    class Meta:
        model = Application
        fields = ['id', 'job', 'user', 'cover_letter', 'resume', 'status', 'applied_at']

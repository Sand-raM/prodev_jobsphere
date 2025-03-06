# jobsphere/job_board/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    # Admin role
    admin_group, created = Group.objects.get_or_create(name='Admin')
    
    # Staff role
    staff_group, created = Group.objects.get_or_create(name='Staff')
    
    # Regular User role
    user_group, created = Group.objects.get_or_create(name='User')

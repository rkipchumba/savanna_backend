from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Customer(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True
    )

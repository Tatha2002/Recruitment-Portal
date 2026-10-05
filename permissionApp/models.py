from django.db import models
from accounts.models import User

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
            unique_together = ("role", "permission")
    
    def __str__(self):
        return f"{self.role} -> {self.permission.name}"
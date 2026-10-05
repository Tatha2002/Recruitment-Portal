from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        'email',
        'name',
        'phone',
        'role',
        'is_verified',
        'is_active',
    )

    list_filter = (
        'role',
        'is_verified',
        'is_active',
    )

    search_fields = (
        'email',
        'name',
        'phone',
    )

    ordering = ('email',)

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),
        ('Personal Information', {
            'fields': (
                'name',
                'phone',
            )
        }),
        ('Role', {
            'fields': (
                'role',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_verified',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'phone',
                'name',
                'password1',
                'password2',
                'role',
                'is_active',
                'is_staff',
                'is_verified',
            ),
        }),
    )
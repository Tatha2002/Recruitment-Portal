from django.contrib import admin
from .models import JobRole, Candidate, ApplicationBatch


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'created_at',
    )

    search_fields = (
        'title',
        'required_skills',
    )


@admin.register(ApplicationBatch)
class ApplicationBatchAdmin(admin.ModelAdmin):

    list_display = (
        'file_name',
        'uploaded_by',
        'total_records',
        'processed_records',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'file_name',
        'uploaded_by__email',
    )


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):

    list_display = (
        'candidate_name',
        'email',
        'phone',
        'college',
        'applied_role',
        'status',
        'expected_salary',
        'created_at',
    )

    list_filter = (
        'status',
        'applied_role',
        'created_at',
    )

    search_fields = (
        'candidate_name',
        'email',
        'phone',
        'college',
        'skills',
    )

    fieldsets = (
        ('Candidate Information', {
            'fields': (
                'candidate_name',
                'email',
                'phone',
                'college',
                'applied_role',
            )
        }),

        ('Professional Information', {
            'fields': (
                'skills',
                'experience_months',
                'notice_period_days',
                'expected_salary',
                'portfolio_url',
                'historical_selection_status',
            )
        }),

        ('Resume and Media', {
            'fields': (
                'resume_text',
                'resume_file',
                'profile_image',
            )
        }),

        ('Screening', {
            'fields': (
                'status',
                'batch',
            )
        }),
    )
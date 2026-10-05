from django.contrib import admin
from .models import InterviewSlot, InterviewFeedback


@admin.register(InterviewSlot)
class InterviewSlotAdmin(admin.ModelAdmin):

    list_display = (
        'role',
        'candidate',
        'interviewer',
        'interview_date',
        'start_time',
        'end_time',
        'status',
    )

    list_filter = (
        'status',
        'role',
        'interview_date',
    )

    search_fields = (
        'candidate__candidate_name',
        'interviewer__email',
    )


@admin.register(InterviewFeedback)
class InterviewFeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'slot',
        'interviewer',
        'rating',
        'recommendation',
        'created_at',
    )

    list_filter = (
        'recommendation',
        'rating',
    )

    search_fields = (
        'slot__candidate__candidate_name',
        'interviewer__email',
    )
from django.db import models
from accounts.models import User
from candidates.models import Candidate, JobRole


class InterviewSlot(models.Model):

    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('BOOKED', 'Booked'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    role = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE,
        related_name='interview_slots'
    )

    interviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='interview_slots'
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interview_slots'
    )

    interview_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.role.title} - {self.interview_date} {self.start_time}"


class InterviewFeedback(models.Model):

    slot = models.OneToOneField(
        InterviewSlot,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    interviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='submitted_feedback'
    )

    rating = models.PositiveIntegerField(
        default=0
    )

    comments = models.TextField(
        blank=True
    )

    recommendation = models.CharField(
        max_length=50,
        choices=(
            ('SELECTED', 'Selected'),
            ('REJECTED', 'Rejected'),
            ('WAITLISTED', 'Waitlisted'),
        ),
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.slot.candidate} - {self.recommendation}"
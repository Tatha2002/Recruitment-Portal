from django.db import models
from accounts.models import User


class JobRole(models.Model):

    title = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    required_skills = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class ApplicationBatch(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='application_batches'
    )

    file_name = models.CharField(
        max_length=255
    )

    total_records = models.PositiveIntegerField(
        default=0
    )

    processed_records = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    error_message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.file_name} - {self.status}"


class Candidate(models.Model):

    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('SHORTLISTED', 'Shortlisted'),
        ('REJECTED', 'Rejected'),
        ('WAITLISTED', 'Waitlisted'),
    )

    candidate_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    college = models.CharField(
        max_length=200
    )

    applied_role = models.ForeignKey(
        JobRole,
        on_delete=models.PROTECT,
        related_name='candidates'
    )

    skills = models.TextField(
        blank=True
    )

    experience_months = models.PositiveIntegerField(
        default=0
    )

    notice_period_days = models.PositiveIntegerField(
        default=0
    )

    expected_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    resume_text = models.TextField(
        blank=True
    )

    portfolio_url = models.URLField(
        blank=True
    )

    historical_selection_status = models.CharField(
        max_length=50,
        blank=True
    )

    resume_file = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='candidate_images/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW'
    )

    batch = models.ForeignKey(
        ApplicationBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='candidates'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.candidate_name} - {self.email}"


class ScreeningResult(models.Model):

    STATUS_CHOICES = [
        ('SHORTLISTED', 'Shortlisted'),
        ('WAITLISTED', 'Waitlisted'),
        ('REJECTED', 'Rejected'),
    ]

    candidate = models.OneToOneField(
        Candidate,
        on_delete=models.CASCADE,
        related_name='screening_result'
    )

    score = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    reason = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.candidate.candidate_name} - {self.status}"



    



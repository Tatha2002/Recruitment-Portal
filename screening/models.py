from django.db import models
from candidates.models import Candidate


class ScreeningResult(models.Model):

    candidate = models.OneToOneField(
        Candidate,
        on_delete=models.CASCADE,
        related_name='screening_result'
    )

    rule_score = models.FloatField(
        default=0
    )

    ml_score = models.FloatField(
        default=0
    )

    nlp_score = models.FloatField(
        default=0
    )

    dl_score = models.FloatField(
        default=0
    )

    final_score = models.FloatField(
        default=0
    )

    prediction = models.CharField(
        max_length=50,
        blank=True
    )

    model_name = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.candidate.candidate_name} - {self.final_score}"
from django.contrib import admin
from .models import ScreeningResult


@admin.register(ScreeningResult)
class ScreeningResultAdmin(admin.ModelAdmin):

    list_display = (
        'candidate',
        'rule_score',
        'ml_score',
        'nlp_score',
        'dl_score',
        'final_score',
        'prediction',
        'created_at',
    )

    list_filter = (
        'prediction',
        'model_name',
    )

    search_fields = (
        'candidate__candidate_name',
        'candidate__email',
    )
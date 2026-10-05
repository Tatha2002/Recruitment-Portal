from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from candidates.models import Candidate


@login_required
@never_cache
def dashboard(request):

    total_candidates = Candidate.objects.count()

    shortlisted = Candidate.objects.filter(
        status='SHORTLISTED'
    ).count()

    rejected = Candidate.objects.filter(
        status='REJECTED'
    ).count()

    new_candidates = Candidate.objects.filter(
        status='NEW'
    ).count()

    role_counts = (
        Candidate.objects
        .values('applied_role__title')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    recent_candidates = (
        Candidate.objects
        .select_related('applied_role')
        .order_by('-created_at')[:5]
    )

    context = {
        'total_candidates': total_candidates,
        'shortlisted': shortlisted,
        'rejected': rejected,
        'new_candidates': new_candidates,
        'role_counts': role_counts,
        'recent_candidates': recent_candidates,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )
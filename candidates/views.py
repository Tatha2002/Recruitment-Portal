from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from django.shortcuts import render
from .models import Candidate, ApplicationBatch, JobRole
from .models import Candidate, ScreeningResult

from .models import Candidate, ScreeningResult
from .screening import calculate_screening_score
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from permissionApp.decorators import permission_required


@login_required
def upload_candidates(request):

    if request.method == 'POST':

        uploaded_file = request.FILES.get('candidate_file')

        if not uploaded_file:
            messages.error(
                request,
                'Please select a CSV file.'
            )
            return redirect('upload_candidates')

        if not uploaded_file.name.lower().endswith('.csv'):
            messages.error(
                request,
                'Please upload a CSV file.'
            )
            return redirect('upload_candidates')

        try:

            # Read uploaded CSV
            decoded_file = uploaded_file.read().decode(
                'utf-8-sig'
            )

            reader = csv.DictReader(
                decoded_file.splitlines()
            )

            rows = list(reader)

        except Exception as e:

            messages.error(
                request,
                f'Unable to read CSV file: {e}'
            )

            return redirect('upload_candidates')


        # Create application batch

        batch = ApplicationBatch.objects.create(
            uploaded_by=request.user,
            file_name=uploaded_file.name,
            total_records=len(rows),
            processed_records=0,
            status='PROCESSING'
        )


        accepted_records = []
        rejected_records = []

        seen_emails = set()


        # Process each candidate

        for row_number, row in enumerate(
            rows,
            start=2
        ):

            try:

                candidate_name = row[
                    'candidate_name'
                ].strip()

                email = row[
                    'email'
                ].strip().lower()

                phone = row[
                    'phone'
                ].strip()

                college = row[
                    'college'
                ].strip()

                applied_role = row[
                    'applied_role'
                ].strip()

                skills = row[
                    'skills'
                ].strip()

                experience_months = int(
                    row[
                        'experience_months'
                    ]
                )

                notice_period_days = int(
                    row[
                        'notice_period_days'
                    ]
                )

                expected_salary = float(
                    row[
                        'expected_salary'
                    ]
                )

                resume_text = row[
                    'resume_text'
                ].strip()

                portfolio_url = row[
                    'portfolio_url'
                ].strip()

                historical_status = row[
                    'historical_selection_status'
                ].strip()


                # -------------------------
                # VALIDATION
                # -------------------------

                if not candidate_name:
                    raise ValueError(
                        'Candidate name is missing'
                    )


                if '@' not in email:
                    raise ValueError(
                        'Invalid email'
                    )


                if not phone.isdigit() or len(phone) != 10:
                    raise ValueError(
                        'Invalid phone number'
                    )


                if email in seen_emails:
                    raise ValueError(
                        'Duplicate candidate'
                    )

                seen_emails.add(email)


                # -------------------------
                # JOB ROLE
                # -------------------------

                job_role, created = JobRole.objects.get_or_create(
                    title=applied_role
                )


                # -------------------------
                # CREATE CANDIDATE
                # -------------------------

                candidate = Candidate.objects.create(

                    candidate_name=candidate_name,

                    email=email,

                    phone=phone,

                    college=college,

                    applied_role=job_role,

                    skills=skills,

                    experience_months=experience_months,

                    notice_period_days=notice_period_days,

                    expected_salary=expected_salary,

                    resume_text=resume_text,

                    portfolio_url=portfolio_url,

                    historical_selection_status=historical_status,

                    batch=batch,

                    status='NEW'
                )


                # Accepted

                accepted_records.append({
                    'candidate_name':
                        candidate.candidate_name,

                    'email':
                        candidate.email,

                    'phone':
                        candidate.phone,

                    'college':
                        candidate.college,

                    'applied_role':
                        candidate.applied_role.title,

                    'status':
                        'ACCEPTED'
                })


            except Exception as e:

                # Rejected

                rejected_records.append({
                    'candidate_name':
                        row.get(
                            'candidate_name',
                            ''
                        ),

                    'email':
                        row.get(
                            'email',
                            ''
                        ),

                    'phone':
                        row.get(
                            'phone',
                            ''
                        ),

                    'reason':
                        str(e)
                })


        # -------------------------
        # UPDATE BATCH
        # -------------------------

        batch.processed_records = (
            len(accepted_records)
            + len(rejected_records)
        )

        batch.status = 'COMPLETED'

        batch.save()


        # -------------------------
        # SHOW RESULT
        # -------------------------

        messages.success(
            request,
            f'{len(accepted_records)} candidates accepted '
            f'and {len(rejected_records)} candidates rejected.'
        )


        return redirect(
            'candidate_list'
        )


    return render(
        request,
        'candidates/upload_candidates.html'
    )


@login_required
def candidate_list(request):

    candidates = Candidate.objects.select_related(
        'applied_role',
        'batch'
    ).all()

    return render(
        request,
        'candidates/candidate_list.html',
        {
            'candidates': candidates
        }
    )


@login_required
@never_cache
# @permission_required('screen_candidate')
def screen_candidate(request, candidate_id):

    candidate = get_object_or_404(
        Candidate,
        id=candidate_id
    )

    score, status, reasons = calculate_screening_score(
        candidate
    )

    ScreeningResult.objects.update_or_create(
        candidate=candidate,
        defaults={
            'score': score,
            'status': status,
            'reason': ', '.join(reasons)
        }
    )

    candidate.status = status

    candidate.save(
        update_fields=['status']
    )

    return redirect(
        'candidate_list'
    )
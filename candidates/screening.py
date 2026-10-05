def calculate_screening_score(candidate):

    score = 0
    reasons = []

    # Experience
    if candidate.experience_months >= 6:
        score += 30
        reasons.append('Good experience')

    elif candidate.experience_months >= 3:
        score += 20
        reasons.append('Moderate experience')

    else:
        score += 10
        reasons.append('Low experience')

    # Skills
    skills = candidate.skills.lower()

    if 'python' in skills:
        score += 25
        reasons.append('Python skill found')

    if 'django' in skills:
        score += 25
        reasons.append('Django skill found')

    if 'sql' in skills:
        score += 10
        reasons.append('SQL skill found')

    # Notice period
    if candidate.notice_period_days <= 30:
        score += 10
        reasons.append('Acceptable notice period')

    # Final status
    if score >= 70:
        status = 'SHORTLISTED'

    elif score >= 50:
        status = 'WAITLISTED'

    else:
        status = 'REJECTED'

    return score, status, reasons
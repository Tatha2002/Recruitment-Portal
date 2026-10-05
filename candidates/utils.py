import re
import pandas as pd
from pathlib import Path


class CandidateIngestionError(Exception):
    """Raised when candidate file processing fails."""
    pass


# Required columns in CSV / Excel file
REQUIRED_COLUMNS = {
    'candidate_name',
    'email',
    'phone',
    'college',
    'applied_role',
    'skills',
    'experience_months',
    'notice_period_days',
    'expected_salary',
    'resume_text',
    'portfolio_url',
    'historical_selection_status',
}


# Email validation
EMAIL_PATTERN = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
)


# Phone validation
PHONE_PATTERN = re.compile(
    r'^\+?[0-9]{10,15}$'
)


def is_valid_email(email):
    return bool(
        EMAIL_PATTERN.fullmatch(
            str(email).strip()
        )
    )


def is_valid_phone(phone):
    return bool(
        PHONE_PATTERN.fullmatch(
            str(phone).strip()
        )
    )


def is_valid_number(value):
    try:
        # Check for empty/NaN value
        if pd.isna(value):
            return False

        number = float(value)

        # Negative numbers are not allowed
        return number >= 0

    except (ValueError, TypeError):
        return False


def clean_string(value):

    if pd.isna(value):
        return ''

    value = str(value).strip()

    # Remove surrounding quotes if present
    value = value.removeprefix('"')
    value = value.removesuffix('"')

    # Remove extra spaces
    value = ' '.join(value.split())

    return value


def clean_row(row):

    cleaned = {}

    for column in REQUIRED_COLUMNS:

        value = row.get(column, '')

        if isinstance(value, str):

            value = clean_string(value)

            # Normalize these fields
            if column in {
                'email',
                'applied_role',
                'skills',
                'historical_selection_status'
            }:
                value = value.lower()

        cleaned[column] = value

    return cleaned


def validate_row(row):

    errors = []

    if not row['candidate_name']:
        errors.append(
            'Candidate name is missing'
        )

    if not is_valid_email(row['email']):
        errors.append(
            'Invalid email'
        )

    if not is_valid_phone(row['phone']):
        errors.append(
            'Invalid phone'
        )

    if not row['college']:
        errors.append(
            'College is missing'
        )

    if not row['applied_role']:
        errors.append(
            'Applied role is missing'
        )

    if not is_valid_number(
        row['experience_months']
    ):
        errors.append(
            'Invalid experience_months'
        )

    if not is_valid_number(
        row['notice_period_days']
    ):
        errors.append(
            'Invalid notice_period_days'
        )

    if not is_valid_number(
        row['expected_salary']
    ):
        errors.append(
            'Invalid expected_salary'
        )

    return errors


def read_candidate_file(file_path):

    file_path = Path(file_path)

    # File does not exist
    if not file_path.exists():
        raise CandidateIngestionError(
            'Uploaded file does not exist'
        )

    # Empty file
    if file_path.stat().st_size == 0:
        raise CandidateIngestionError(
            'Uploaded file is empty'
        )

    extension = file_path.suffix.lower()

    # Read CSV
    if extension == '.csv':

        df = pd.read_csv(file_path)

    # Read Excel
    elif extension in ['.xlsx', '.xls']:

        df = pd.read_excel(file_path)

    else:

        raise CandidateIngestionError(
            'Only CSV and Excel files are supported'
        )

    # No rows
    if df.empty:
        raise CandidateIngestionError(
            'Uploaded file contains no records'
        )

    return df


def validate_columns(df):

    actual_columns = set(df.columns)

    missing_columns = (
        REQUIRED_COLUMNS - actual_columns
    )

    if missing_columns:

        raise CandidateIngestionError(
            'Missing required columns: '
            + ', '.join(
                sorted(missing_columns)
            )
        )


def find_duplicate_emails(rows):

    seen = set()
    duplicates = set()

    for row in rows:

        email = row['email']

        if email in seen:

            duplicates.add(email)

        else:

            seen.add(email)

    return duplicates


def process_candidate_file(
    file_path,
    output_directory
):

    # Read file
    df = read_candidate_file(
        file_path
    )

    # Check columns
    validate_columns(df)

    accepted_rows = []
    rejected_rows = []

    # Convert DataFrame to list
    rows = df.to_dict(
        'records'
    )

    # Clean all rows first
    cleaned_rows = [
        clean_row(row)
        for row in rows
    ]

    # Find duplicate emails
    duplicate_emails = find_duplicate_emails(
        cleaned_rows
    )

    # Validate each row
    for cleaned in cleaned_rows:

        errors = validate_row(
            cleaned
        )

        # Duplicate email
        if cleaned['email'] in duplicate_emails:

            errors.append(
                'Duplicate email'
            )

        # Rejected
        if errors:

            rejected = cleaned.copy()

            rejected['rejection_reason'] = (
                '; '.join(errors)
            )

            rejected_rows.append(
                rejected
            )

        # Accepted
        else:

            accepted_rows.append(
                cleaned
            )

    # Create output directory
    output_directory = Path(
        output_directory
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # Output files
    accepted_file = (
        output_directory /
        'accepted_rows.csv'
    )

    rejected_file = (
        output_directory /
        'rejected_rows.csv'
    )

    # Save accepted records
    pd.DataFrame(
        accepted_rows
    ).to_csv(
        accepted_file,
        index=False
    )

    # Save rejected records
    pd.DataFrame(
        rejected_rows
    ).to_csv(
        rejected_file,
        index=False
    )

    return {
        'accepted': accepted_rows,
        'rejected': rejected_rows,
        'accepted_file': str(
            accepted_file
        ),
        'rejected_file': str(
            rejected_file
        ),
    }
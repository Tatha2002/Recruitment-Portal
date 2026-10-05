# HR Candidate Screening System

An HR Candidate Screening System built with **Django** to simplify the candidate recruitment and screening process.

The system allows HR users to upload candidate information through CSV files, validate candidate data, manage application batches, and automatically screen candidates based on predefined criteria.

---

## 🚀 Features

### Candidate Management

* Upload candidate information using CSV
* Validate candidate data
* Detect duplicate candidates
* Validate email and phone numbers
* Store candidate information in the database
* View all uploaded candidates
* Track candidate status

### Application Batch Management

Each CSV upload creates an application batch containing:

* File name
* Total records
* Processed records
* Upload status
* Upload date
* Uploaded by

Supported batch statuses:

* Pending
* Processing
* Completed
* Failed

### Job Role Management

The system manages job roles with:

* Role title
* Job description
* Required skills
* Candidate mapping

### Candidate Screening

Candidates can be screened individually.

The screening system calculates:

* Candidate score
* Screening status
* Screening reasons

Possible screening results:

* **Shortlisted**
* **Waitlisted**
* **Rejected**

The candidate's current status is automatically updated after screening.

### HR Dashboard

The dashboard provides an overview of:

* Total candidates
* New candidates
* Shortlisted candidates
* Rejected candidates
* Role-wise candidate count
* Recent candidates

### Authentication & Permissions

The system includes:

* User authentication
* Login protection
* Permission-based candidate screening
* Role/permission management

Only users with the required screening permission can perform candidate screening.

---

## 🛠️ Technology Stack

### Backend

* Python
* Django
* Django REST Framework

### Database

* PostgreSQL

### Frontend

* HTML
* CSS
* Bootstrap
* Django Templates

### Other Technologies

* CSV processing
* Django ORM
* Django Authentication
* Custom permission system

---

## 📁 Project Structure

```text
project/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── candidates/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── screening.py
│   └── ...
│
├── permissionApp/
│   ├── models.py
│   ├── decorators.py
│   └── ...
│
├── interviews/
│   └── ...
│
├── dashboard/
│   └── ...
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── candidates/
│       ├── upload_candidates.html
│       └── candidate_list.html
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 📊 Candidate Data

The system accepts candidate data through a CSV file.

Example fields:

```text
candidate_name
email
phone
college
applied_role
skills
experience_months
notice_period_days
expected_salary
resume_text
portfolio_url
historical_selection_status
```

Example:

```csv
candidate_name,email,phone,college,applied_role,skills,experience_months,notice_period_days,expected_salary,resume_text,portfolio_url,historical_selection_status
Rahul Sharma,rahul@gmail.com,9876543210,ABC College,Python Django Developer,"python,django,sql,git",12,30,500000,"Python Django developer with SQL experience",https://github.com/rahul,selected
```

---

## 🔄 Application Workflow

```text
HR Login
   │
   ▼
Dashboard
   │
   ▼
Upload Candidates CSV
   │
   ▼
CSV Validation
   │
   ├── Invalid / Duplicate
   │       ↓
   │    Rejected
   │
   └── Valid
           ↓
      Candidate Created
           ↓
      Status = NEW
           ↓
      Candidate List
           ↓
      Screen Candidate
           ↓
      Calculate Score
           ↓
   ┌───────┼───────────┐
   │       │           │
   ▼       ▼           ▼
Shortlisted Waitlisted Rejected
```

---

## 🧠 Screening Process

The screening logic is implemented in:

```text
candidates/screening.py
```

The screening function evaluates candidate information and returns:

```python
score, status, reasons
```

The result is stored in the `ScreeningResult` model.

Example:

```text
Score: 85
Status: SHORTLISTED
Reason: Python skill matched, Django experience, relevant experience
```

The candidate's status is then updated automatically.

---

## 🗄️ Main Database Models

### JobRole

Stores available job roles.

```text
title
description
required_skills
created_at
```

### ApplicationBatch

Stores information about each uploaded CSV batch.

```text
uploaded_by
file_name
total_records
processed_records
status
error_message
created_at
```

### Candidate

Stores candidate information.

```text
candidate_name
email
phone
college
applied_role
skills
experience_months
notice_period_days
expected_salary
resume_text
portfolio_url
historical_selection_status
resume_file
profile_image
status
batch
created_at
updated_at
```

### ScreeningResult

Stores the result of candidate screening.

```text
candidate
score
status
reason
created_at
updated_at
```

---

## ⚙️ Installation

### 1. Clone the repository

```text
git clone <your-repository-url>
```

### 2. Open the project

```text
cd <project-folder>
```

### 3. Create a virtual environment

```text
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```text
venv\Scripts\activate
```

### 5. Install dependencies

```text
pip install -r requirements.txt
```

### 6. Configure the database

Update the database configuration in:

```text
settings.py
```

with your PostgreSQL credentials.

### 7. Run migrations

```text
python manage.py makemigrations
python manage.py migrate
```

### 8. Create an admin user

```text
python manage.py createsuperuser
```

### 9. Start the development server

```text
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 🔐 Permissions

Candidate screening is protected using a custom permission:

```text
screen_candidate
```

The screening view checks the permission before allowing the screening operation.

This prevents unauthorized users from performing candidate screening.

---

## 📌 Candidate Status Flow

Initially, every successfully uploaded candidate is:

```text
NEW
```

After screening:

```text
NEW
 ↓
SHORTLISTED
```

or:

```text
NEW
 ↓
WAITLISTED
```

or:

```text
NEW
 ↓
REJECTED
```

---

## 🎯 Future Improvements

Possible future enhancements include:

* Resume PDF upload and parsing
* NLP-based resume analysis
* AI/ML-based candidate ranking
* Advanced filtering
* Interview scheduling
* Email notifications
* Candidate search
* Pagination
* Export screened candidates to CSV
* HR analytics and charts
* REST API
* Background processing using Celery and Redis

---

## 👨‍💻 Author

**Tathagata Das**

B.Tech Computer Science

---

## 📄 License

This project is developed for educational and recruitment management purposes.

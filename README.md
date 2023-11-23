# Applicant Tracking System (ATS)

This system is designed to  automate various aspects of the hiring process, from adding resumes to a database to analyzing candidate qualifications based on scores and scheduling interview appointments for eligible candidates.

## Features
### 1. Authentication
   - **User Authentication:** The system includes an authentication mechanism to control access. Users need to log in with valid token to access the system.

### 2. Job Management
   - **Job Listing Page:** View and manage all job positions, with the ability to save them in the database.

### 3. Requirements and Skills
   - **Job Requirements :** Specify the requirements and skills for each job, including a scoring system that will be used to evaluate candidate resumes.

### 4. HR Approval
   - **HR Approval Page:** HR personnel can review and approve submitted forms. If approved, the system automatically notifies the Technical Director of the relevant department to review and add interviewers. If rejected, there is a message field for feedback.

### 5. Technical Director(TD) Approval
   - **TD Approval Page:** TDs can approve forms and add interviewers.

### 6. Resume Upload and Analysis
   - **Resume Upload by HR:** HR can upload an Excel file containing links to online resumes. The system extracts relevant information and adds the links and job positions and etc to the database.
   - **Score Calculation:** The system calculates scores for candidates based on job requirements. Candidates with eligible scores initiates the interview scheduling process.

### 7. Interview Scheduling
   - **Interview Appointment Page:** The system schedules interview appointments for eligible candidates and sends confirmation emails with the interview time to the candidates.

### 8. Old Candidate Updates
   - **Invite Old Candidates:**   HR can set job titles to filter and automatically send an email, including a form, to old candidates with the relevant job title to update their resumes and approve.
   - **Interview Appointment for Old Candidates:** Interview appointments are automatically set for old candidates who approve the form and are eligible based on the score.
     
### 9. Candidate List
   - **Candidate List Page:** View a list of all candidates stored in the database.

## Getting Started

These instructions will help you set up and run the project on your local machine. 

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/niluws/ATS.git
   cd ATS
   ```

2. Create a virtual environment and activate it:

   ```shell
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```shell
   pip install -r Requirements.txt
   ```

4. Set up your PostgreSQL database and configure your settings in the `settings.py` file.

5. Migrate the database:

   ```shell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Run the development server:

   ```shell
   python manage.py runserver
   ```

7. Start Redis and PostgreSQL containers using Docker:

   ```shell
   docker-compose up -d
   ```

8. Your project should now be accessible at [http://localhost:8000/](http://localhost:8000/).

## Technologies Used

- [Python](https://www.python.org/downloads/)
- [Django](https://www.djangoproject.com/)
- [Redis](https://redis.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)

# Eco-Nexus: Integrated Education and Career Hub

Eco-Nexus is a comprehensive Django-based web application designed to bridge the gap between education and careers, with a special emphasis on sustainability and environmental studies. It integrates a University Management System (UMS), a Learning Management System (LMS), and a Career Services portal into a single, cohesive platform.

## Core Features

The platform is built around three main modules:

### 1. University Management System (UMS)
The UMS handles the academic backbone of the institution.
-   **Course Management**: Create and manage courses, assigning them to departments and semesters.
-   **Departments & Semesters**: Organize the academic structure of the university.
-   **Enrollment**: Allows students to enroll in courses.
-   **Grading**: Facilitates the submission and tracking of student grades.

### 2. Learning Management System (LMS)
The LMS provides an interactive online learning environment, with a focus on environmental education.
-   **Environmental Courses**: Specialized courses focused on sustainability.
-   **Modular Learning**: Courses are broken down into modules, containing lessons with text and video content.
-   **Interactive Quizzes**: Each module can have quizzes to test student knowledge.
-   **Gamification**: Students earn points and badges for completing courses and quizzes, which contributes to their "Green Profile".

### 3. Career Services
The careers portal connects students with employers, particularly those in the green economy.
-   **Job Postings**: Employers can post job opportunities.
-   **Student Applications**: Students can apply for jobs, uploading their resume and cover letter.
-   **Employer Profiles**: Companies can create profiles to attract talent.
-   **Green Profile**: A unique feature that showcases a student's sustainability-related achievements, skills, and scores derived from the LMS, making them more attractive to eco-conscious employers.

## Screenshots

*(Add screenshots of the application here. You can use markdown like this:)*

**Landing Page:**
![Landing Page]('/static/screencapture-127-0-0-1-8000-2025-11-22-15_20_30.png')

**Student Dashboard:**
![Student Dashboard]('/static/screencapture-127-0-0-1-8000-accounts-profile-2025-11-22-15_21_59.png')

**Course Detail:**
![Course Detail]('/static/screencapture-127-0-0-1-8000-ums-courses-2025-11-22-15_20_58.png')

## Technical Stack

-   **Backend**: Django
-   **Frontend**: HTML, Tailwind CSS
-   **Database**: SQLite (for development), configurable for production
-   **Apps**: The project is modular, with separate Django apps for `accounts`, `ums`, `lms`, and `careers`.

## Getting Started

To get the project up and running locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd 'Final Project'
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/Scripts/activate  # On Windows
    # source .venv/bin/activate  # On macOS/Linux
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file would need to be generated using `pip freeze > requirements.txt`)*

4.  **Configure environment variables:**
    Create a `.env` file in the project root and add the following:
    ```
    SECRET_KEY='your-secret-key'
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Load initial data (optional):**
    Fixtures for initial data (like users, courses, jobs) may be available.
    ```bash
    python manage.py loaddata users.json departments.json semesters.json courses.json ...
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

## Application Structure

-   `eco_nexus/`: The main Django project directory containing `settings.py` and `urls.py`.
-   `accounts/`: Handles user authentication, profiles, and the `StudentProfile` model.
-   `ums/`: The University Management System application.
-   `lms/`: The Learning Management System application.
-   `careers/`: The Career Services and job board application.
-   `theme/`: The Tailwind CSS theme application.
-   `templates/`: Contains the main HTML templates.
-   `static/`: Contains static assets like CSS, JS, and images.
-   `manage.py`: The Django command-line utility.

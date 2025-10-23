# django_auth_system

## A role-based authentication platform built with Django, supporting custom user profiles (Patient/Doctor), real-time signup validation, profile images, and dedicated role dashboards. Modern UI and extensible codebase for health, care, or enterprise portals.
## Features
- **Custom User Model**: Extends Django’s User to support patient/doctor roles, email as a unique identifier, phone, and address info.

- **Role-Based Dashboards**: Directs users to distinct dashboards based on their type (Patient or Doctor) after login.

- **Modern Signup & Auth**:

  - AJAX-powered real-time username/email availability checks.

  - Password strength validation and confirmation as you type.

  - Profile picture upload support.

  - Clean, responsive UI.

- **Security & Best Practices**:

  - Custom authentication forms.

  - CSRF protection and validation.

  - Robust password policies.

- **Admin Portal**: Fully integrated for managing users via Django’s Admin panel.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Nitish-Biswas/django_auth_system.git
cd django_auth_system
```

### 2. Setup the virtual environment
```bash
  python -m venv venv
  # Activate your backend virtual environment first:
  
  # On Windows:
  venv\Scripts\activate
  
  # On macOS/Linux:
  source venv/bin/activate
```

### 3. Run migrations to set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the development server:
```bash
python manage.py runserver
```

### 5. Access the app:
Open http://127.0.0.1:8000/ in your browser to see the login page. Sign up as either a Patient or Doctor to explore the role dashboards!


## Project Structure
- ```auth_project/```: Main Django project configuration.

- ```users/```: Handles authentication logic, custom user model, forms, views, and role-based dashboards.

- ```templates/```: HTML templates for auth pages and dashboards.

- ```static/```: Stylesheets and assets for the UI.

- ```media/```: User-uploaded profile pictures.

- ```manage.py```, ```requirements.txt```: Core Django setup.

## Core Functionalities
- **Flexible Accounts**: Supports patients and doctors with different dashboards.

- **AJAX Validation**: Checks username/email for duplicates live during signup.

- **Profile Management**: Complete address and contact info, profile picture upload.

- **Secure**: Enforces strong passwords and user uniqueness.

- **Clean UI**: Responsive, mobile-friendly forms and dashboards.

## Support
For issues and questions:
• Create an issue on GitHub

You can also contact the developer:
• **Name**: Nitish Biswas
• **Email**: nitishbiswas066@gmail.com
• **Linkedin**: [nitish-biswas1](https://www.linkedin.com/in/nitish-biswas1/)

---

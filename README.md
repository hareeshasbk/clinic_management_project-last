# Clinic Management System

## Overview

This project is a **Clinic Management System** developed as a final-year Computer Science diploma engineering project. It provides a comprehensive solution for managing appointments, tracking medications, and implementing role-based user access in a clinic environment. The system is built using Django (a Python web framework), SQLite (for development), and Bootstrap (for the front-end).

---

## Key Features

### User Management
- User registration with role selection (Admin, Doctor, Patient, Receptionist)
- Login/Logout functionality
- Role-Based Access Control (RBAC) with dashboards for different roles
- Password reset functionality

### Appointment Scheduling
- Appointment booking functionality
- Integration with Flatpickr for date and time selection
- Doctor's upcoming appointments displayed

### Medication Tracking
- Admin-only management of medications (Add, Edit, Delete)
- Doctors can create and manage prescriptions for patients
- List views for medications and prescriptions
- Patient prescription tracking
- Basic inventory tracking for medications

### Security
- Input validation to prevent XSS and injection attacks
- Password hashing for secure storage
- Email OTP-based Two-Factor Authentication (2FA) for login

### Other Features
- Containerization using Docker

---

## Technologies Used

| **Component**        | **Technology**           |
|-----------------------|--------------------------|
| Backend              | Django (Python framework)|
| Database             | SQLite (for development) |
| Frontend             | HTML, CSS, JavaScript, Bootstrap |
| Date/Time Picker     | `django-flatpickr`       |
| 2FA                  | Email OTP                |

---

## Project Structure

```
clinic_management_project/
├── venv/                   # Virtual environment folder
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
├── .gitignore              # Untracked files ignored by Git
├── .dockerignore           # Files excluded from Docker image
├── clinic_management/      # Main Django project directory
│   ├── settings.py         # Project settings
│   ├── urls.py             # URL configurations
│   ├── asgi.py
│   └── wsgi.py
├── users/                  # Django app for user management
│   ├── models.py           # User models
│   ├── views.py            # Views for user actions
│   ├── urls.py             # URL configurations
│   ├── rbac_config.py      # RBAC configurations
│   └── forms.py            # User forms
├── appointments/           # Django app for scheduling appointments
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── medications/            # Django app for tracking medications
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── static/                 # Static files (CSS, JavaScript, images)
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── account/            # Authentication templates
│   ├── users/              # User-related templates
│   ├── appointments/       # Appointment templates
│   └── medications/        # Medication templates
├── Dockerfile              # Docker image build instructions
└── LICENSE.md              # Licensing information
```


## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/hareeshasbk/clinic-management-system.git
   cd clinic-management-project  # Adjust to match your folder name
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Django:**
   ```bash
   pip install Django
   ```

5. **Install Dependencies:**
   After installing Django, use the following command to install all other required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create a Superuser (Optional):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the Application:**
   Open your browser and go to: [http://localhost:8000/](http://localhost:8000/)

---

## Security Considerations

- **Input Validation:** Prevents XSS and other injection attacks.
- **Password Hashing:** Uses Django’s built-in authentication system for secure password storage.
- **HTTPS:** Use HTTPS in deployment to encrypt communication (see the "HTTPS and SSL/TLS Implementation" section).
- **RBAC:** Limits access to sensitive features and data based on user roles.

---

## Future Enhancements

- Implement automated unit testing.
- Add 2FA to the login page for enhanced security.

---

## Contact

**Hareesh Bhat**  
Email: [hareesha.sbk@gmail.com](mailto:hareesha.sbk@gmail.com)

---

## License

This project is licensed under the [License Name] License. See the `LICENSE.md` file for more details.

---

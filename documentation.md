# MediConnect API Documentation

This document provides a comprehensive overview of the MediConnect API endpoints, categorized by user roles: Patients, Doctors, and Admins.

## Patients

- **Authentication**
    - `POST /login/access-token`: Obtain an access token.
    - `POST /login/test-token`: Test the validity of an access token.
- **User Management**
    - `GET /users/me`: Get the current user's information.
    - `PUT /users/me`: Update the current user's information.
    - `GET /users/{user_id}`: Get another user's public information.
- **Appointments**
    - `GET /appointments`: Get a list of the patient's appointments.
    - `POST /appointments`: Create a new appointment.
    - `GET /appointments/{appointment_id}`: Get the details of a specific appointment.
    - `PUT /appointments/{appointment_id}`: Update an appointment.
    - `DELETE /appointments/{appointment_id}`: Cancel an appointment.
- **Consultations**
    - `GET /consultations`: Get a list of the patient's consultations.
    - `GET /consultations/{consultation_id}`: Get the details of a specific consultation.
- **Reviews**
    - `POST /reviews`: Create a new review for a doctor.
- **Notifications**
    - `GET /notifications`: Get a list of the patient's notifications.
- **AI Features**
    - `POST /ai/symptom-checker`: Use the AI-powered symptom checker.

## Doctors

- **Authentication**
    - `POST /login/access-token`: Obtain an access token.
    - `POST /login/test-token`: Test the validity of an access token.
- **User Management**
    - `GET /users/me`: Get the current user's information.
    - `PUT /users/me`: Update the current user's information.
- **Doctor Profile**
    - `GET /doctors/me`: Get the doctor's own profile.
    - `PUT /doctors/me`: Update the doctor's profile.
- **Appointments**
    - `GET /appointments`: Get a list of the doctor's appointments.
    - `GET /appointments/{appointment_id}`: Get the details of a specific appointment.
    - `PUT /appointments/{appointment_id}`: Update an appointment.
- **Consultations**
    - `GET /consultations`: Get a list of the doctor's consultations.
    - `POST /consultations`: Create a new consultation.
    - `GET /consultations/{consultation_id}`: Get the details of a specific consultation.
    - `PUT /consultations/{consultation_id}`: Update a consultation.
- **Notifications**
    - `GET /notifications`: Get a list of the doctor's notifications.

## Admins

- **Authentication**
    - `POST /login/access-token`: Obtain an access token.
- **Admin Dashboard**
    - `GET /admin/dashboard-stats`: Get key performance indicators for the dashboard.
- **Doctor Applications**
    - `GET /admin/doctor-applications`: Get a list of doctor applications.
    - `PATCH /admin/doctor-applications/{app_id}`: Approve or reject a doctor application.
- **User Management**
    - `GET /admin/users`: Get a list of all users.
    - `PATCH /admin/users/{user_id}`: Update a user's information.
    - `DELETE /admin/users/{user_id}`: Delete a user.
- **Hospital Management**
    - `GET /admin/hospitals`: Get a list of all hospitals.
    - `POST /admin/hospitals`: Create a new hospital.
    - `PUT /admin/hospitals/{hospital_id}`: Update a hospital.
    - `DELETE /admin/hospitals/{hospital_id}`: Delete a hospital.
    - `POST /admin/hospitals/import`: Bulk-import hospitals from a CSV/Excel file.
- **Medication Management**
    - `GET /admin/medications`: Get a list of all medications.
    - `POST /admin/medications`: Create a new medication.
    - `PUT /admin/medications/{medication_id}`: Update a medication.
    - `DELETE /admin/medications/{medication_id}`: Delete a medication.
    - `GET /admin/medications/export-template`: Download a template for bulk-importing medications.
- **Notifications**
    - `POST /admin/broadcast-notification`: Send a notification to a group of users.
- **Income Management**
    - `GET /admin/income/stats`: Get income statistics.
    - `GET /admin/income/chart-data`: Get data for income charts.
    - `GET /admin/income/transactions`: Get a list of all transactions.
- **Permissions**
    - `GET /admin/permissions`: Get a list of all permissions.
    - `POST /admin/permissions`: Create a new permission.

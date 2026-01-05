# MediConnect Doctor Module - API Specification

## 1. Introduction

This document specifies the RESTful API endpoints required for the Doctor module of the MediConnect application. These endpoints will power the doctor-facing features, replacing the existing mock data services.

All endpoints prefixed with `/api/v1/doctors/me/` require **Doctor Role authentication** via a JWT Bearer token. Other shared and public endpoints are also referenced for completeness.

---

## 2. Authentication & Onboarding

Doctors use the main authentication endpoints for registration and login, with an additional verification flow.

-   **`POST /api/v1/auth/signup`**: Registers a new user with the role set to `DOCTOR`.
-   **`POST /api/v1/auth/login/access-token`**: Authenticates a doctor and returns a JWT.

### 2.1. Doctor Verification Flow

-   **`POST /api/v1/doctors/me/documents`**: (Multipart/Form-Data) Allows a newly registered doctor to upload their medical license and degree certificate for verification.
-   **`GET /api/v1/doctors/me/verification-status`**: Allows a doctor to check their current verification status (`pending`, `approved`, `rejected`).

---

## 3. API Endpoints

### 3.1. Doctor Dashboard (`/api/v1/doctors/me/`)

#### `GET /dashboard-stats`

-   **Description**: Fetches all key performance indicators (KPIs) and recent data for the main doctor dashboard.
-   **Success Response (200)**:
    ```json
    {
      "todaysAppointments": 5,
      "totalPatients": 120,
      "thisMonthsIncome": 4500.50,
      "pendingReports": 3
    }
    ```

### 3.2. Profile & Settings (`/api/v1/doctors/me/`)

-   **`GET /profile`**: Fetches the complete, detailed profile for the currently logged-in doctor.
-   **`PUT /profile`**: Updates the profile of the currently logged-in doctor.

### 3.3. Schedule & Appointments (`/api/v1/doctors/me/`)

-   **`GET /appointments`**: Retrieves a list of all appointments for the logged-in doctor, with filters for status and date range.
-   **`GET /appointments/{appointment_id}`**: Retrieves the details of a single appointment.
-   **`PATCH /appointments/{appointment_id}`**: Allows a doctor to cancel or reschedule an appointment.
-   **`POST /appointments/{appointment_id}/consultation`**: Finalizes a consultation, submitting all details including SOAP notes, treatment plans, prescriptions, etc. The request body should match the `ConsultationDetails` schema.

### 3.4. Patient Management (`/api/v1/doctors/me/`)

-   **`GET /patients`**: Retrieves a list of all unique patients associated with the doctor.
-   **`GET /patients/{patient_id}/history`**: Retrieves a specific patient's complete history, including all past appointments and consultation details.
-   **`POST /patients`**: Manually creates a new patient record in the system.
-   **`POST /soap-notes`**: Creates a standalone SOAP note for a patient, not tied to a specific scheduled appointment.

### 3.5. Practice Management (`/api/v1/doctors/me/`)

#### Hospital Schedules
-   **`GET /hospital-schedules`**: Lists all hospital schedules for the doctor.
-   **`POST /hospital-schedules`**: Creates a new hospital schedule.
-   **`PUT /hospital-schedules/{schedule_id}`**: Updates a hospital schedule.
-   **`DELETE /hospital-schedules/{schedule_id}`**: Deletes a hospital schedule.

#### Income Tracking
-   **`GET /income/stats`**: Retrieves key financial metrics (total, monthly, etc.).
-   **`GET /income/chart-data`**: Retrieves data formatted for revenue charts.
-   **`GET /income/transactions`**: Retrieves a list of recent financial transactions.

### 3.6. Shared Clinical Tools

These endpoints are also used by other modules but are critical for doctors.

-   **`GET /api/v1/medicines`**: (Public) Searchable and paginated access to the global medicine database.
-   **`POST /api/v1/ai/report-analysis`**: (JWT Auth) Submits a patient's medical report (image/PDF) for AI analysis.
-   **`POST /api/v1/ai/interaction-checker`**: (JWT Auth) Submits a list of medicines to check for potential drug-drug interactions.

### 3.7. Subscriptions

-   **`GET /api/v1/subscriptions/plans/doctor`**: Retrieves all available subscription plans for doctors.
-   **`POST /api/v1/subscriptions/purchase`**: Handles the purchase of a recurring subscription. The request body specifies the `planId`.
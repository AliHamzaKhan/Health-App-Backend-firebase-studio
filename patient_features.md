# MediConnect Patient Module - API Specification

## 1. Introduction

This document specifies the RESTful API endpoints required for the Patient module of the MediConnect application. The frontend is fully implemented, and these endpoints will replace the current mock data services.

All endpoints prefixed with `/api/v1/patients/me/` require **Patient Role authentication** via a JWT Bearer token. Public endpoints for searching doctors and hospitals are also listed for completeness.

---

## 2. Authentication & Signup

Patients use the main authentication endpoints for registration and login.

-   **`POST /api/v1/auth/signup`**: Registers a new user with the role set to `PATIENT`. The request body will contain all fields from the patient signup form.
-   **`POST /api/v1/auth/login/access-token`**: Authenticates a patient and returns a JWT.

All subsequent requests to protected patient endpoints must include the `Authorization: Bearer <access_token>` header.

---

## 3. API Endpoints

### 3.1. Profile Management (`/api/v1/patients/me/`)

Endpoints for managing the authenticated patient's own profile.

#### `GET /profile`

-   **Description**: Fetches the complete, detailed profile for the currently logged-in patient.
-   **Success Response (200)**:
    ```json
    {
      "id": "user-1",
      "name": "Jane Doe",
      "email": "jane.doe@example.com",
      "role": "patient",
      "profilePic": "https://picsum.photos/seed/patient/100/100",
      "phone": "555-0101",
      "dateOfBirth": "1992-07-15",
      "gender": "Female",
      "bloodType": "O+",
      "height": 165,
      "weight": 60,
      "allergies": ["Peanuts", "Pollen"],
      "medicalConditions": ["Asthma"],
      "emergencyContactName": "John Doe",
      "emergencyContactPhone": "555-0100"
    }
    ```

#### `PUT /profile`

-   **Description**: Updates the profile of the currently logged-in patient.
-   **Request Body**: A JSON object with any of the fields from the `GET /profile` response that are updatable.
-   **Success Response (200)**: The updated patient profile object.

### 3.2. Appointments (`/api/v1/patients/me/appointments`)

Endpoints for managing appointments from the patient's perspective.

#### `GET /`

-   **Description**: Retrieves a list of all appointments for the logged-in patient, with filtering.
-   **Query Parameters**:
    -   `status` (optional, string): Filter by status. Enum: `upcoming`, `completed`, `cancelled`.
-   **Success Response (200)**: An array of appointment objects.

#### `POST /`

-   **Description**: Books a new appointment with a doctor.
-   **Request Body**:
    ```json
    {
      "doctorId": "doc-1",
      "date": "2024-08-15",
      "time": "14:30",
      "reason": "Annual check-up"
    }
    ```
-   **Success Response (201)**: The newly created appointment object.

#### `GET /{appointment_id}`

-   **Description**: Retrieves the details of a single appointment.
-   **Success Response (200)**: The full appointment object, including consultation notes if completed.

#### `PATCH /{appointment_id}`

-   **Description**: Allows a patient to cancel or confirm completion of an appointment.
-   **Request Body**:
    ```json
    // To cancel
    { "status": "cancelled" }
    
    // To confirm completion (if enabled)
    { "status": "completed" }
    ```
-   **Success Response (200)**: The updated appointment object.

### 3.3. Health Search (Public)

These are public endpoints used within the patient dashboard.

-   **`GET /api/v1/doctors`**: Search for doctors with filters (location, specialty, name).
-   **`GET /api/v1/doctors/{doctor_id}`**: Get a doctor's public profile and reviews.
-   **`POST /api/v1/doctors/{doctor_id}/reviews`**: Submit a review for a doctor after a completed appointment.
-   **`GET /api/v1/hospitals`**: Search for hospitals.
-   **`GET /api/v1/hospitals/{hospital_id}`**: Get a hospital's public profile.

### 3.4. Health Tracking (`/api/v1/patients/me/`)

Endpoints for logging and retrieving personal health data.

#### `GET/POST /vitals`

-   **Description**: `GET` to retrieve all vital logs, `POST` to add a new one.
-   **POST Request Body**:
    ```json
    {
      "bloodPressureSystolic": 120,
      "bloodPressureDiastolic": 80,
      "heartRate": 72,
      "bloodSugar": 95,
      "weight": 60.5
    }
    ```
-   **Success Response**: The created vital log (for POST) or an array of logs (for GET).

#### `GET/POST/PUT/DELETE /medications`

-   **Description**: Full CRUD for the patient's personal medication schedule.
-   **POST/PUT Request Body**:
    ```json
    {
      "name": "Lisinopril",
      "dosage": "10mg",
      "instructions": "Take one tablet in the morning.",
      "times": ["08:00"]
    }
    ```

#### `POST /medications/log`

-   **Description**: Marks a specific medication dose as taken for the day.
-   **Request Body**:
    ```json
    {
      "medicationId": "med-1",
      "time": "08:00",
      "date": "2024-07-30",
      "isTaken": true
    }
    ```
-   **Success Response (200)**: `{ "status": "success" }`

### 3.5. AI Health Tools (`/api/v1/ai/`)

These endpoints consume AI tokens from the user's account.

-   **`POST /report-analysis`**: Takes multipart/form-data with one or more files. Analyzes medical reports. **Costs tokens**.
-   **`POST /symptom-checker`**: Analyzes user-described symptoms. **Costs tokens**.
-   **`POST /allergy-checker`**: Checks an item against the user's registered allergies. **Costs tokens**.
-   **`POST /calorie-checker`**: Analyzes an image of food to estimate calories. **Costs tokens**.

### 3.6. Token & Subscription Management

#### `GET /api/v1/patients/me/tokens`

-   **Description**: Retrieves the user's current token balance and transaction history.
-   **Success Response (200)**:
    ```json
    {
      "balance": 120,
      "history": [
        { "id": "txn-1", "description": "Welcome bonus", "tokenChange": 10, "date": "..." }
      ]
    }
    ```

#### `GET /api/v1/subscriptions/plans/patient`

-   **Description**: Retrieves all available subscription plans for patients.
-   **Success Response (200)**: An array of `SubscriptionPlan` objects.

#### `POST /api/v1/subscriptions/purchase`

-   **Description**: Handles the purchase of a one-time token pack or a recurring subscription.
-   **Request Body**:
    ```json
    {
      "type": "package", // or "subscription"
      "planId": "otp-2" // ID of the package or plan
    }
    ```
-   **Success Response (200)**: `{ "status": "success", "message": "Purchase successful." }`
# MediConnect Schedule Management - API Specification

## 1. Introduction

This document provides a detailed specification for the RESTful API endpoints that handle appointment and schedule management within the MediConnect application. These endpoints are essential for the core functionality of booking, viewing, modifying, and documenting clinical appointments. They serve both the Patient and Doctor modules of the frontend application.

---

## 2. Authentication & Authorization

All endpoints listed in this document are protected and require a valid **JWT Bearer token** in the `Authorization` header. Access to each endpoint is further restricted by user role (`PATIENT` or `DOCTOR`), as specified in the endpoint descriptions. Unauthorized or forbidden requests should return `401 Unauthorized` or `403 Forbidden` HTTP status codes, respectively.

---

## 3. Core Data Models (JSON Schemas)

These Pydantic-style schemas define the JSON objects used in API requests and responses.

### `Appointment` (Response Model)

The full appointment object returned by the API.

```json
{
  "id": "appt-1",
  "patient_id": 1,
  "doctor_id": 2,
  "patient_name": "Jane Doe",
  "patient_photo": "https://picsum.photos/seed/patient/100/100",
  "doctor_name": "Dr. John Smith",
  "doctor_photo": "https://picsum.photos/seed/doctor/100/100",
  "doctor_specialty": "Cardiology",
  "date": "2024-08-15",
  "time": "10:30 AM",
  "status": "UPCOMING",
  "reason": "Annual check-up",
  "notes": null,
  "review_given": false,
  "consultation_details": null
}
```
**Status Enum**: `UPCOMING`, `COMPLETED`, `CANCELLED`

### `AppointmentCreate` (Patient Request)

Used by a patient to book a new appointment.

```json
{
  "doctor_id": 2,
  "date": "2024-08-15",
  "time": "10:30",
  "reason": "Annual check-up"
}
```

### `AppointmentUpdate` (Patient/Doctor Request)

Used to modify an existing appointment (e.g., cancel or reschedule).

```json
{
  "date": "2024-08-20",
  "time": "11:00",
  "status": "CANCELLED"
}
```
*Note: Fields are optional. Only provided fields will be updated.*

### `ConsultationCreate` (Doctor Request)

Used by a doctor to finalize a consultation and add clinical notes.

```json
{
    "hpi": "Patient reports intermittent chest pain over the last month.",
    "soap_note": "S: Patient reports chest pain. O: BP 130/85. A: Suspected angina. P: Prescribe Nitroglycerin.",
    "icd_codes": "I20.9, R07.9",
    "treatment_plan": "Start with lifestyle modifications. Follow up in 1 month.",
    "prescribed_medicines": [
        { "name": "Nitroglycerin", "dosage": "0.4mg", "frequency": "As needed for chest pain" }
    ],
    "recommended_lab_tests": ["Lipid Panel", "Troponin I"],
    "referral": "Dr. Eva Green, Interventional Cardiologist"
}
```

---

## 4. Patient Endpoints

These endpoints are scoped to the currently authenticated patient.

**API Prefix**: `/api/v1/patients/me/`

| Method | Endpoint | Description | Auth Role |
| --- | --- | --- | --- |
| `GET` | `/appointments` | Retrieves a list of the patient's own appointments. | `PATIENT` |
| `POST`| `/appointments` | Books a new appointment with a specified doctor. | `PATIENT` |
| `GET` | `/appointments/{appointment_id}` | Retrieves the full details of a single appointment. | `PATIENT` |
| `PATCH`| `/appointments/{appointment_id}` | Allows the patient to cancel their upcoming appointment. | `PATIENT` |

---

### `GET /appointments`

-   **Description**: Fetches all appointments for the logged-in patient, with optional filtering by status.
-   **Query Parameters**:
    -   `status` (optional, string): Filter by status. Enum: `upcoming`, `completed`, `cancelled`. If omitted, should return all.
-   **Success Response (200 OK)**: An array of `Appointment` objects.
-   **Error Responses**: `401 Unauthorized`.

### `POST /appointments`

-   **Description**: Creates a new appointment record.
-   **Request Body**: `AppointmentCreate` object.
-   **Success Response (201 Created)**: The newly created `Appointment` object.
-   **Error Responses**: `400 Bad Request` (e.g., invalid data, slot unavailable), `401 Unauthorized`, `404 Not Found` (if `doctor_id` is invalid).

### `GET /appointments/{appointment_id}`

-   **Description**: Fetches the complete details for a specific appointment belonging to the patient.
-   **Success Response (200 OK)**: A single `Appointment` object.
-   **Error Responses**: `401 Unauthorized`, `403 Forbidden` (if appointment does not belong to user), `404 Not Found`.

### `PATCH /appointments/{appointment_id}`

-   **Description**: Used by the patient to update their appointment, primarily for cancellation.
-   **Request Body**:
    ```json
    {
      "status": "CANCELLED"
    }
    ```
-   **Success Response (200 OK)**: The updated `Appointment` object.
-   **Error Responses**: `400 Bad Request` (e.g., trying to cancel a completed appointment), `401 Unauthorized`, `403 Forbidden`.

---

## 5. Doctor Endpoints

These endpoints are scoped to the currently authenticated doctor.

**API Prefix**: `/api/v1/doctors/me/`

| Method | Endpoint | Description | Auth Role |
| --- | --- | --- | --- |
| `GET` | `/appointments` | Retrieves a list of the doctor's appointments. | `DOCTOR` |
| `GET` | `/appointments/{appointment_id}` | Retrieves the full details of a single appointment. | `DOCTOR` |
| `PATCH`| `/appointments/{appointment_id}` | Reschedules or cancels an appointment. | `DOCTOR` |
| `POST` | `/appointments/{appointment_id}/consultation` | Finalizes a consultation and saves clinical notes. | `DOCTOR` |
| `POST` | `/appointments/follow-up` | Schedules a new follow-up appointment for a patient. | `DOCTOR` |

---

### `GET /appointments`

-   **Description**: Fetches all appointments assigned to the logged-in doctor, with filtering.
-   **Query Parameters**:
    -   `status` (optional, string): `upcoming`, `completed`, `cancelled`.
    -   `startDate` (optional, string): `YYYY-MM-DD` format.
    -   `endDate` (optional, string): `YYYY-MM-DD` format.
    -   `page` / `size` (optional, int): For pagination.
-   **Success Response (200 OK)**: A paginated response object containing an array of `Appointment` objects.

### `GET /appointments/{appointment_id}`

-   **Description**: Fetches the complete details for a specific appointment assigned to the doctor, including full patient details.
-   **Success Response (200 OK)**: A single `Appointment` object with extended `patientDetails`.
-   **Error Responses**: `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

### `PATCH /appointments/{appointment_id}`

-   **Description**: Used by the doctor to update an appointment (reschedule or cancel).
-   **Request Body**: `AppointmentUpdate` object.
-   **Success Response (200 OK)**: The updated `Appointment` object.
-   **Error Responses**: `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`.

### `POST /appointments/{appointment_id}/consultation`

-   **Description**: Marks an `UPCOMING` appointment as `COMPLETED` and attaches the detailed clinical notes from the consultation. This is a critical endpoint for finalizing a patient visit.
-   **Request Body**: `ConsultationCreate` object.
-   **Success Response (200 OK)**: The updated `Appointment` object, now with `status: "COMPLETED"` and the full `consultation_details`.
-   **Error Responses**: `400 Bad Request` (if appointment is not upcoming), `401 Unauthorized`, `403 Forbidden`.

### `POST /appointments/follow-up`

-   **Description**: Allows a doctor to book a subsequent appointment for a patient, typically after a consultation.
-   **Request Body**:
    ```json
    {
      "patient_id": 1,
      "date": "2024-09-15",
      "time": "11:00",
      "reason": "Follow-up for blood pressure monitoring"
    }
    ```
-   **Success Response (201 Created)**: The newly created `Appointment` object.
-   **Error Responses**: `400 Bad Request`, `401 Unauthorized`, `404 Not Found` (if `patient_id` is invalid).

# MediConnect SOAP Note & Clinical Recording - API Specification

## 1. Introduction

This document provides a detailed specification for the RESTful API endpoints that handle the creation, generation, and management of clinical documentation, specifically focusing on SOAP (Subjective, Objective, Assessment, Plan) notes. These endpoints are a core part of the Doctor module and integrate AI capabilities for enhanced productivity.

---

## 2. Authentication & Authorization

All endpoints listed in this document are protected and require a valid **JWT Bearer token** in the `Authorization` header. Access is restricted to users with the `DOCTOR` role. Unauthorized or forbidden requests should return `401 Unauthorized` or `403 Forbidden` HTTP status codes, respectively.

---

## 3. Core Data Models (JSON Schemas)

These schemas define the primary JSON objects used in API requests and responses for clinical documentation.

### `ConsultationDetails` (Request Model)

The comprehensive payload submitted to document a clinical encounter. This is used when finalizing a scheduled appointment or creating a standalone note.

```json
{
    "hpi": "Patient reports intermittent chest pain over the last month, especially after exertion.",
    "soap_note": "S: Patient reports chest pain with exertion, describes it as a pressure. O: BP 130/85, HR 88. Lungs clear. No pedal edema. A: Suspected stable angina. P: Prescribe Nitroglycerin, recommend stress test.",
    "icd_codes": "I20.9, R07.9",
    "treatment_plan": "Start with lifestyle modifications including low-sodium diet and increased physical activity. Follow up in 1 month to review stress test results.",
    "prescribed_medicines": [
        { "name": "Nitroglycerin", "dosage": "0.4mg", "frequency": "As needed for chest pain" },
        { "name": "Aspirin", "dosage": "81mg", "frequency": "Once daily" }
    ],
    "recommended_lab_tests": ["Lipid Panel", "Troponin I", "ECG Stress Test"],
    "referral": "Dr. Eva Green, Interventional Cardiologist"
}
```

### `StandaloneSoapNoteCreate` (Request Model)

Used to create a clinical record for an unscheduled encounter, like a walk-in or phone call.

```json
{
  "patient_id": 123,
  "date": "2024-07-31",
  "reason": "Walk-in: Suture Removal",
  "consultation_details": {
    "hpi": "Patient returns for suture removal 10 days post-laceration repair.",
    "soap_note": "S: Patient reports no pain or signs of infection. O: Wound is clean, dry, and intact. Good healing noted. A: Healed laceration. P: Sutures removed without complication. Advised to keep area clean.",
    "icd_codes": "Z48.02",
    "treatment_plan": "No further follow-up required unless signs of infection develop.",
    "prescribed_medicines": [],
    "recommended_lab_tests": [],
    "referral": null
  }
}
```

### `SoapNoteGenerationResponse` (Response Model)

The structured response from the AI SOAP note generation endpoint.

```json
{
  "generated_text": "S: Patient complains of a persistent dry cough and mild fever for the last 3 days...\nO: Temperature: 100.4°F, BP: 120/80 mmHg...\nA: Suspected viral upper respiratory infection...\nP: Prescribed rest, hydration, and OTC fever reducers..."
}
```

---

## 4. API Endpoints

### 4.1. AI-Powered Generation

#### `POST /api/v1/ai/generate-soap-note`

-   **Description**: Takes a recorded audio file of a patient-doctor conversation and uses the Gemini API to transcribe it and generate a structured SOAP note.
-   **Authentication**: `DOCTOR` role required.
-   **Request Type**: `multipart/form-data`.
    -   `audio_file`: The audio file (e.g., in `.webm`, `.mp3`, or `.wav` format).
    -   `context` (optional, string): Additional text context, such as patient name and a brief summary of their history, to improve the accuracy of the AI-generated note.
-   **Success Response (200 OK)**: A `SoapNoteGenerationResponse` object.
-   **Error Responses**:
    -   `400 Bad Request`: If no audio file is provided.
    -   `401 Unauthorized` / `403 Forbidden`.
    -   `500 Internal Server Error`: If the call to the Gemini API fails.

### 4.2. Clinical Documentation

#### `POST /api/v1/doctors/me/appointments/{appointment_id}/consultation`

-   **Description**: Finalizes a scheduled consultation. This endpoint associates the detailed clinical notes with the appointment and updates the appointment's status to `COMPLETED`.
-   **Authentication**: `DOCTOR` role required.
-   **Request Body**: A `ConsultationDetails` object.
-   **Success Response (200 OK)**: The full, updated `Appointment` object, now including the `consultationDetails` and a status of `COMPLETED`.
-   **Error Responses**:
    -   `400 Bad Request`: If the appointment is not in an `UPCOMING` state or if the request body is invalid.
    -   `404 Not Found`: If the `appointment_id` does not exist or does not belong to the doctor.

#### `POST /api/v1/doctors/me/soap-notes`

-   **Description**: Creates a new, standalone clinical record for a patient that is not tied to a pre-existing appointment. This is for documenting unscheduled encounters. The backend should handle this by creating a new `Appointment` record that is immediately marked as `COMPLETED`.
-   **Authentication**: `DOCTOR` role required.
-   **Request Body**: A `StandaloneSoapNoteCreate` object.
-   **Success Response (201 Created)**: The newly created and completed `Appointment` object.
-   **Error Responses**:
    -   `400 Bad Request`: If the request body is invalid.
    -   `404 Not Found`: If the specified `patient_id` does not exist.

#### `GET /api/v1/doctors/me/patients/{patient_id}/history`

-   **Description**: Retrieves the complete clinical history for a specific patient, including all past completed appointments and their associated consultation details (which contain the SOAP notes).
-   **Authentication**: `DOCTOR` role required.
-   **Success Response (200 OK)**: An array of completed `Appointment` objects, sorted in descending order by date.
-   **Error Responses**:
    -   `404 Not Found`: If the `patient_id` does not exist.

---

## 5. Frontend Workflow for AI SOAP Note Generation

This section describes the expected sequence of API calls from the frontend to implement the AI recording feature within a consultation.

1.  **Start Recording**: The doctor clicks the "Start Recording" button in the frontend. The browser's `MediaRecorder` API is used to capture audio from the microphone.
2.  **Stop Recording**: The doctor stops the recording. The frontend now has the complete audio data as a `Blob` object.
3.  **Call AI Generation Endpoint**: The frontend creates a `FormData` object, appends the audio `Blob` as `audio_file`, and makes a `POST` request to `/api/v1/ai/generate-soap-note`.
4.  **Receive Generated Text**: The backend processes the audio with the Gemini API and returns a `SoapNoteGenerationResponse` containing the structured SOAP note text.
5.  **Populate Form**: The frontend takes the `generated_text` from the response and populates the `soapNote` textarea in the consultation form.
6.  **Review and Finalize**: The doctor reviews the AI-generated note, makes any necessary edits or additions to it and other fields in the form (prescriptions, treatment plan, etc.).
7.  **Submit Consultation**: The doctor clicks "Finalize Consultation".
8.  **Save Documentation**: The frontend sends the entire `ConsultationDetails` form data in a `POST` request to `/api/v1/doctors/me/appointments/{appointment_id}/consultation`.
9.  **Confirmation**: The backend saves all the clinical details, updates the appointment status, and returns the updated appointment object, confirming the successful completion of the encounter.

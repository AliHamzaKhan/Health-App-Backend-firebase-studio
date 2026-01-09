import os
import json
import google.genai as genai
from google.genai import types
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.schemas.ai import Report, ReportSummary, SoapNoteGenerationResponse, AIModel, AIModelCreate
from app.schemas.ai_features import (
    ReportAnalysisRequest, ReportAnalysisResponse,
    SymptomCheckerRequest, SymptomCheckerResponse,
    AllergyCheckerRequest, AllergyCheckerResponse,
    CalorieCheckerRequest, CalorieCheckerResponse
)
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_ai
from typing import List
from app.schemas.response import StandardResponse

# Configure the Gemini API key

router = APIRouter()


def _upload_to_gemini(file_path: str, mime_type: str, display_name: str):
    """
    Uploads a file to Gemini using the NEW google.genai SDK
    """

    client = genai.Client()

    file = client.files.upload(
        file=file_path,  # ✅ CORRECT ARGUMENT NAME
        config=types.UploadFileConfig(
            mime_type=mime_type,
            display_name=display_name,
        )
    )

    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


@router.post("/generate-soap-note", response_model=StandardResponse[SoapNoteGenerationResponse])
async def generate_soap_note(
    audio_file: UploadFile = File(...),
    context: str = Form(None),
):
    if not audio_file:
        return StandardResponse(success=False, message="No audio file provided.")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(audio_file.filename)[1],
        ) as tmp:
            tmp.write(await audio_file.read())
            tmp_path = tmp.name

        uploaded_file = _upload_to_gemini(
            file_path=tmp_path,
            mime_type=audio_file.content_type,
            display_name=audio_file.filename,
        )

        client = genai.Client()

        prompt = (
            "Please transcribe the following audio and generate a SOAP note. "
            f"Context: {context}"
        )

        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[prompt, uploaded_file],
        )

    except Exception as e:
        return StandardResponse(success=False, message=f"An error occurred while generating the SOAP note: {e}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return StandardResponse(
        data=SoapNoteGenerationResponse(generated_text=response.text),
        message="SOAP note generated successfully.",
    )


@router.post("/report/text-analysis", response_model=StandardResponse[ReportSummary])
async def analyze_text_report(reports: List[Report]):
    try:
        client = genai.Client()

        compiled_report = "\n\n".join(
            f"""
            Report Title: {r.title}
            Patient ID: {r.patient_id}
            Summary: {r.summary}
            Recommendations: {r.recommendations}
            """
            for r in reports
        )

        prompt = (
            "You are a medical AI assistant.\n"
            "Analyze the following medical reports and produce a concise, unified summary "
            "highlighting key findings, risks, and next steps.\n\n"
            f"{compiled_report}"
        )

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt],
        )

        summary = response.text

    except Exception as e:
        return StandardResponse(
            success=False,
            message=f"Text report analysis failed: {e}",
        )

    return StandardResponse(
        data=ReportSummary(summary=summary),
        message="Text reports analyzed successfully.",
    )



@router.post("/report/file-analysis", response_model=StandardResponse[ReportSummary])
async def analyze_file_report(
    images: List[UploadFile] = File(...),
):
    tmp_paths = []

    try:
        client = genai.Client()
        uploaded_files = []

        # 1️⃣ Save + upload each image
        for image in images:
            suffix = os.path.splitext(image.filename)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await image.read())
                tmp_paths.append(tmp.name)

            uploaded = _upload_to_gemini(
                file_path=tmp.name,
                mime_type=image.content_type,
                display_name=image.filename,
            )

            uploaded_files.append(uploaded)

        # 2️⃣ Build Gemini contents
        contents = [
            "Analyze the following medical report images and provide a concise summary."
        ]
        contents.extend(uploaded_files)

        # 3️⃣ Gemini call
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=contents,
        )

        summary = response.text

    except Exception as e:
        return StandardResponse(
            success=False,
            message=f"Image report analysis failed: {e}",
        )

    finally:
        # 4️⃣ Cleanup temp files
        for path in tmp_paths:
            if os.path.exists(path):
                os.remove(path)

    return StandardResponse(
        data=ReportSummary(summary=summary),
        message="Image report analyzed successfully.",
    )




@router.post("/symptom-checker", response_model=StandardResponse[SymptomCheckerResponse])
async def symptom_checker(request: SymptomCheckerRequest):
    try:
        client = genai.Client()

        prompt = (
            "Analyze the following symptoms and return JSON with keys "
            "'assessment' and 'recommended_action'.\n\n"
            f"Symptoms: {request.symptoms}"
        )

        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[prompt],
        )

        response_json = json.loads(response.text)

    except Exception as e:
        return StandardResponse(success=False, message=f"An error occurred while checking symptoms: {e}")

    return StandardResponse(
        data=SymptomCheckerResponse(
            assessment=response_json.get("assessment"),
            recommended_action=response_json.get("recommended_action"),
        ),
        message="Symptom check successful.",
    )


@router.post("/allergy-checker", response_model=StandardResponse[AllergyCheckerResponse])
async def allergy_checker(request: AllergyCheckerRequest):
    try:
        client = genai.Client()

        prompt = (
            "Determine if the following could be an allergic reaction. "
            "Return JSON with keys: is_allergy, confidence, potential_allergens.\n\n"
            f"Symptoms: {', '.join(request.symptoms)}\n"
            f"Medical History: {', '.join(request.medical_history)}"
        )

        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[prompt],
        )

        response_json = json.loads(response.text)

    except Exception as e:
        return StandardResponse(success=False, message=f"An error occurred while checking for allergies: {e}")

    return StandardResponse(
        data=AllergyCheckerResponse(
            is_allergy=response_json.get("is_allergy"),
            confidence=response_json.get("confidence"),
            potential_allergens=response_json.get("potential_allergens"),
        ),
        message="Allergy check successful.",
    )


@router.post("/calorie-checker", response_model=StandardResponse[CalorieCheckerResponse])
async def calorie_checker(request: CalorieCheckerRequest):
    try:
        client = genai.Client()

        prompt = (
            "Provide calorie count and macronutrient breakdown in JSON.\n\n"
            f"Food item: {request.meal_description}"
        )

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt],
        )

        response_json = json.loads(response.text)

    except Exception as e:
        return StandardResponse(success=False, message=f"An error occurred while checking calories: {e}")

    return StandardResponse(
        data=CalorieCheckerResponse(
            calories=response_json.get("calories"),
            breakdown=response_json.get("breakdown"),
        ),
        message="Calorie check successful.",
    )


@router.post("/ai-models/", response_model=StandardResponse[AIModel])
def create_ai_model(
        *,
        db: Session = Depends(deps.get_db),
        ai_model_in: AIModelCreate,
):
    """
    Create new AI model.
    """
    ai_model = crud_ai.create_ai_model(db=db, ai_model=ai_model_in)
    return StandardResponse(data=ai_model, message="AI model created successfully.")


@router.get("/ai-models/{ai_model_id}", response_model=StandardResponse[AIModel])
def read_ai_model(
        *,
        db: Session = Depends(deps.get_db),
        ai_model_id: int,
):
    """
    Get AI model by ID.
    """
    ai_model = crud_ai.get_ai_model(db=db, ai_model_id=ai_model_id)
    if not ai_model:
        return StandardResponse(success=False, message="AI Model not found")
    return StandardResponse(data=ai_model, message="AI model retrieved successfully.")


@router.get("/ai-models/", response_model=StandardResponse[List[AIModel]])
def read_ai_models(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
):
    """
    Retrieve AI models.
    """
    ai_models = crud_ai.get_ai_models(db=db, skip=skip, limit=limit)
    return StandardResponse(data=ai_models, message="AI models retrieved successfully.")

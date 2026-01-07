import os
import json
import google.genai as genai
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
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

# Configure the Gemini API key

router = APIRouter()

def _upload_to_gemini(file_path: str, mime_type: str):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """

    file = genai.upload_file(path=file_path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

@router.post("/analyze_report", response_model=ReportSummary)
async def analyze_report(report: Report):
    """
    Analyzes a medical report using the Gemini API to generate a summary.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Please analyze the following medical report and provide a concise summary:\n\n{report.report}"
        response = model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while analyzing the report: {e}")
    return ReportSummary(summary=summary)

@router.post("/generate-soap-note", response_model=SoapNoteGenerationResponse)
async def generate_soap_note(
    audio_file: UploadFile = File(...),
    context: str = Form(None)
):
    """
    Generates a SOAP note from an audio file using the Gemini API.
    """
    if not audio_file:
        raise HTTPException(status_code=400, detail="No audio file provided.")

    try:
        # Write the audio file to a temporary location
        with open(audio_file.filename, "wb") as f:
            f.write(audio_file.file.read())
        
        # Upload the audio file to Gemini
        uploaded_file = _upload_to_gemini(audio_file.filename, audio_file.content_type)

        # Transcribe the audio and generate the SOAP note
        model = genai.GenerativeModel(model_name="gemini-pro")
        prompt = f"Please transcribe the following audio and generate a SOAP note based on the content. Context: {context}"
        response = model.generate_content([prompt, uploaded_file])
        
        # Clean up the temporary file
        os.remove(audio_file.filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the SOAP note: {e}")

    return SoapNoteGenerationResponse(generated_text=response.text)


@router.post("/report-analysis", response_model=ReportAnalysisResponse)
async def report_analysis(request: ReportAnalysisRequest):
    """
    Analyzes a medical report using the Gemini API to provide a summary.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Please analyze the following medical report and provide a summary:\n\n{request.report}"
        response = model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while analyzing the report: {e}")
    return ReportAnalysisResponse(summary=summary)

@router.post("/symptom-checker", response_model=SymptomCheckerResponse)
async def symptom_checker(request: SymptomCheckerRequest):
    """
    Checks symptoms using the Gemini API and provides an assessment and recommended action.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Please analyze the following symptoms and provide a potential diagnosis and recommended action in JSON format. The JSON should have two keys: 'assessment' and 'recommended_action'.\n\nSymptoms: {request.symptoms}"
        response = model.generate_content(prompt)
        response_json = json.loads(response.text)
        assessment = response_json.get("assessment")
        recommended_action = response_json.get("recommended_action")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while checking symptoms: {e}")
    return SymptomCheckerResponse(assessment=assessment, recommended_action=recommended_action)

@router.post("/allergy-checker", response_model=AllergyCheckerResponse)
async def allergy_checker(request: AllergyCheckerRequest):
    """
    Checks for allergies using the Gemini API and provides an assessment, confidence level, and potential allergens.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Please analyze the following symptoms and medical history and determine if they could cause an allergic reaction. Provide the answer in JSON format with three keys: 'is_allergy' (boolean), 'confidence' (float between 0 and 1), and 'potential_allergens' (a list of strings).\n\nSymptons: {', '.join(request.symptoms)}\n\nMedical History: {', '.join(request.medical_history)}"
        response = model.generate_content(prompt)
        response_json = json.loads(response.text)
        is_allergy = response_json.get("is_allergy")
        confidence = response_json.get("confidence")
        potential_allergens = response_json.get("potential_allergens")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while checking for allergies: {e}")
    return AllergyCheckerResponse(is_allergy=is_allergy, confidence=confidence, potential_allergens=potential_allergens)

@router.post("/calorie-checker", response_model=CalorieCheckerResponse)
async def calorie_checker(request: CalorieCheckerRequest):
    """
    Checks the calorie count of a food item using the Gemini API.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Please provide the calorie count and a macronutrient breakdown (protein, carbohydrates, and fat) for the following food item in JSON format. The JSON should have two keys: 'calories' (integer) and 'breakdown' (a dictionary with keys 'protein', 'carbohydrates', and 'fat').\n\nFood item: {request.meal_description}"
        response = model.generate_content(prompt)
        response_json = json.loads(response.text)
        calories = response_json.get("calories")
        breakdown = response_json.get("breakdown")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while checking calories: {e}")
    return CalorieCheckerResponse(calories=calories, breakdown=breakdown)

@router.post("/ai-models/", response_model=AIModel)
def create_ai_model(
    *,
    db: Session = Depends(deps.get_db),
    ai_model_in: AIModelCreate,
):
    """
    Create new AI model.
    """
    ai_model = crud_ai.create_ai_model(db=db, ai_model=ai_model_in)
    return ai_model


@router.get("/ai-models/{ai_model_id}", response_model=AIModel)
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
        raise HTTPException(status_code=404, detail="AI Model not found")
    return ai_model


@router.get("/ai-models/", response_model=List[AIModel])
def read_ai_models(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve AI models.
    """
    ai_models = crud_ai.get_ai_models(db=db, skip=skip, limit=limit)
    return ai_models

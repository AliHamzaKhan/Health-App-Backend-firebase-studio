
from sqlalchemy.orm import Session
from app.models.ai import AIModel
from app.schemas.ai import AIModelCreate

def create_ai_model(db: Session, ai_model: AIModelCreate):
    db_ai_model = AIModel(**ai_model.dict())
    db.add(db_ai_model)
    db.commit()
    db.refresh(db_ai_model)
    return db_ai_model

def get_ai_model(db: Session, ai_model_id: int):
    return db.query(AIModel).filter(AIModel.id == ai_model_id).first()

def get_ai_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AIModel).offset(skip).limit(limit).all()

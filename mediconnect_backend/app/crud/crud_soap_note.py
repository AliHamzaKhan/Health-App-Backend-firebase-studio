from app.crud.crud_base import CRUDBase
from app.models.soap_note import SoapNote
from app.schemas.soap_notes import SoapNoteCreate, SoapNoteUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class CRUDSoapNote(CRUDBase[SoapNote, SoapNoteCreate, SoapNoteUpdate]):
    async def create_with_owner(self, db: AsyncSession, *, obj_in: SoapNoteCreate, doctor_id: int) -> SoapNote:
        db_obj = self.model(**obj_in.dict(), doctor_id=doctor_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

crud_soap_note = CRUDSoapNote(SoapNote)

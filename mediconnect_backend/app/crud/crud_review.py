from app.crud.crud_base import CRUDBase
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.db.base import Review

class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    pass

crud_review = CRUDReview(Review)

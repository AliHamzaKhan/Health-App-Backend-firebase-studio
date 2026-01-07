from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_review import crud_review
from app.schemas.review import Review, ReviewCreate, ReviewUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Review])
async def read_reviews(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve reviews.
    """
    reviews = await crud_review.get_multi(db, skip=skip, limit=limit)
    return reviews


@router.get("/{review_id}", response_model=Review)
async def read_review(
    review_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific review by ID.
    """
    review = await crud_review.get(db, id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.delete("/{review_id}", response_model=Review)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a review.
    """
    review = await crud_review.get(db, id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review = await crud_review.remove(db, id=review_id)
    return review

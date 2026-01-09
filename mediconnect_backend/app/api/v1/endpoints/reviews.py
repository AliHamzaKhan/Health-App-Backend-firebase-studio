from fastapi import APIRouter, Depends
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_review import crud_review
from app.schemas.review import Review, ReviewCreate, ReviewUpdate
from app.models.user import User
from app.schemas.response import StandardResponse
from app import crud

router = APIRouter()


@router.post("/", response_model=StandardResponse[Review])
async def create_review(
    *,
    db: AsyncSession = Depends(deps.get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new review.
    """
    review = await crud_review.create_with_owner(db=db, obj_in=review_in, owner_id=current_user.id)
    return StandardResponse(data=review, message="Review created successfully.")


@router.get("/", response_model=StandardResponse[List[Review]])
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
    return StandardResponse(data=reviews, message="Reviews retrieved successfully.")


@router.get("/{review_id}", response_model=StandardResponse[Review])
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
        return StandardResponse(success=False, message="Review not found")
    return StandardResponse(data=review, message="Review retrieved successfully.")


@router.put("/{review_id}", response_model=StandardResponse[Review])
async def update_review(
    *,
    db: AsyncSession = Depends(deps.get_db),
    review_id: int,
    review_in: ReviewUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a review.
    """
    review = await crud_review.get(db=db, id=review_id)
    if not review:
        return StandardResponse(success=False, message="Review not found")
    if review.user_id != current_user.id and not crud.crud_user.is_superuser(current_user):
        return StandardResponse(success=False, message="Not enough permissions")
    review = await crud_review.update(db=db, db_obj=review, obj_in=review_in)
    return StandardResponse(data=review, message="Review updated successfully.")


@router.delete("/{review_id}", response_model=StandardResponse[Review])
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
        return StandardResponse(success=False, message="Review not found")
    review = await crud_review.remove(db, id=review_id)
    return StandardResponse(data=review, message="Review deleted successfully.")

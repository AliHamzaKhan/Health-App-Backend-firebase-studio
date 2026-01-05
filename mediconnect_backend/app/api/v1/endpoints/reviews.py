from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_review import crud_review
from app.schemas.review import ReviewCreate, ReviewUpdate, Review

router = APIRouter()

@router.post("/reviews", response_model=Review)
async def create_review(
    *,
    db: AsyncSession = Depends(deps.get_db),
    review_in: ReviewCreate
):
    review = await crud_review.create(db, obj_in=review_in)
    return review

@router.get("/reviews/{id}", response_model=Review)
async def get_review(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    review = await crud_review.get(db, id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/reviews", response_model=List[Review])
async def get_all_reviews(db: AsyncSession = Depends(deps.get_db)):
    return await crud_review.get_multi(db)

@router.put("/reviews/{id}", response_model=Review)
async def update_review(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    review_in: ReviewUpdate
):
    review = await crud_review.get(db, id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review = await crud_review.update(db, db_obj=review, obj_in=review_in)
    return review

@router.delete("/reviews/{id}", response_model=Review)
async def delete_review(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    review = await crud_review.get(db, id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review = await crud_review.remove(db, id=id)
    return review

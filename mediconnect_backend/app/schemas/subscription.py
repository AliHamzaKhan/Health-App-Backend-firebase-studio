from pydantic import BaseModel
from typing import Literal, Optional

class SubscriptionBase(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    features: Optional[list[str]] = None

class SubscriptionCreate(SubscriptionBase):
    name: str
    price: float
    features: list[str]

class SubscriptionUpdate(SubscriptionBase):
    pass

class SubscriptionInDBBase(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True

class Subscription(SubscriptionInDBBase):
    pass

class SubscriptionPurchase(BaseModel):
    type: Literal["package", "subscription"]
    planId: str

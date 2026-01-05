from pydantic import BaseModel
from typing import Literal

class SubscriptionPurchase(BaseModel):
    type: Literal["package", "subscription"]
    planId: str

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class NotificationBase(BaseModel):
    user_id: int
    message: str

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(NotificationBase):
    read: bool

class Notification(NotificationBase):
    id: int
    created_at: datetime
    read: bool

    model_config = ConfigDict(from_attributes=True)

class NotificationBroadcast(BaseModel):
    message: str
    target_audience: str
    audience_role: Optional[str] = None

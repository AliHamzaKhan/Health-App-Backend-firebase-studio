from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

DataType = TypeVar('DataType')

class StandardResponse(BaseModel, Generic[DataType]):
    success: bool = Field(True, description="Indicates if the request was successful.")
    data: Optional[DataType] = Field(None, description="The data payload of the response.")
    message: str = Field("Operation successful.", description="A message providing details about the response.")

    class Config:
        arbitrary_types_allowed = True
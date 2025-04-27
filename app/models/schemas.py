from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Dict, Optional, TypedDict, Literal, Any, List
import re

class WorkflowState(TypedDict):
    user_query: str
    user_query_history: List[str] = []
    license_plate: Optional[str]
    location: Optional[str]
    provided_license_plate: Optional[str]
    provided_location: Optional[str]
    
    access_code: Optional[str]
    provided_access_code: Optional[str]
    final_message: Optional[str]
    end_of_conversation: bool = False

class CollectInformationSchema(BaseModel):
    license_plate: Optional[str] = Field(description="License plate number of the vehicle")
    location: Optional[str] = Field(description="Location of the vehicle")
    access_code: Optional[str] = Field(description="Access code for the vehicle")


class GetAccessCodeSchema(BaseModel):
    access_code: Optional[str] = Field(description="Access code for the user")



class ChatMessage(BaseModel):
    """Chat message input model with validation"""
    model_config = ConfigDict(
        extra="forbid", 
        validate_assignment=True,
        str_strip_whitespace=True
    )
    
    user_id: str = Field(
        ..., 
        description="User identifier (e.g., phone number)",
        min_length=3,
        max_length=50,
        examples=["user123", "+1234567890"]
    )
    text: str = Field(
        ..., 
        description="Message text content",
        min_length=1,
        max_length=500
    )
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user_id format"""
        if not re.match(r'^[a-zA-Z0-9+_\-@.]+$', v):
            raise ValueError('user_id contains invalid characters')
        return v

class ChatResponse(BaseModel):
    """Chat response model"""
    model_config = ConfigDict(
        extra="forbid"
    )
    
    user_id: str = Field(..., description="User identifier")
    message: str = Field(..., description="Response message")
    end: bool = Field(..., description="End of conversation")
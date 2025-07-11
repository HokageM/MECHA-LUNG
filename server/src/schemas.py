from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Doctor Schemas
class DoctorCreate(BaseModel):
    """Schema for creating a new doctor"""
    user_name: str
    password: str

class DoctorLogin(BaseModel):
    """Schema for doctor login"""
    user_name: str
    password: str

class DoctorResponse(BaseModel):
    """Schema for doctor response (without password)"""
    id: int
    user_name: str
    created_at: Optional[str]
    is_active: bool

class DoctorUpdate(BaseModel):
    """Schema for updating doctor information"""
    user_name: Optional[str] = None
    is_active: Optional[bool] = None

# Patient Data Schemas
class PatientDataCreate(BaseModel):
    """Schema for creating patient data"""
    name: str
    age: int
    biological_gender: bool
    smoking: bool
    yellow_fingers: bool
    anxiety: bool
    peer_pressure: bool
    chronic_disease: bool
    fatigue: bool
    allergy: bool
    wheezing: bool
    alcohol: bool
    coughing: bool
    shortness_of_breath: bool
    swallowing_difficulty: bool
    chest_pain: bool

class PatientDataResponse(BaseModel):
    """Schema for patient data response"""
    id: int
    name: str  # Decrypted name
    age: int
    biological_gender: bool
    smoking: bool
    yellow_fingers: bool
    anxiety: bool
    peer_pressure: bool
    chronic_disease: bool
    fatigue: bool
    allergy: bool
    wheezing: bool
    alcohol: bool
    coughing: bool
    shortness_of_breath: bool
    swallowing_difficulty: bool
    chest_pain: bool
    lung_cancer: bool
    prediction_confidence: Optional[float]
    doctor_id: int
    created_at: Optional[str]

class PatientDataUpdate(BaseModel):
    """Schema for updating patient data"""
    name: Optional[str] = None
    age: Optional[int] = None
    biological_gender: Optional[bool] = None
    smoking: Optional[bool] = None
    yellow_fingers: Optional[bool] = None
    anxiety: Optional[bool] = None
    peer_pressure: Optional[bool] = None
    chronic_disease: Optional[bool] = None
    fatigue: Optional[bool] = None
    allergy: Optional[bool] = None
    wheezing: Optional[bool] = None
    alcohol: Optional[bool] = None
    coughing: Optional[bool] = None
    shortness_of_breath: Optional[bool] = None
    swallowing_difficulty: Optional[bool] = None
    chest_pain: Optional[bool] = None

# Authentication Schemas
class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str
    user: DoctorResponse

class TokenData(BaseModel):
    """Schema for token payload data"""
    user_name: Optional[str] = None

# API Response Schemas
class APIResponse(BaseModel):
    """Generic API response schema"""
    message: str
    status: str = "success"
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    status_code: int 
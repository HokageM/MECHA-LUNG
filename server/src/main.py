from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import timedelta

from db.database import Engine, SessionLocal
from db.models import Base, Doctor, PatientData
from security import create_access_token, verify_token
from config import settings
from schemas import (
    DoctorCreate, 
    DoctorLogin, 
    DoctorResponse, 
    DoctorUpdate,
    PatientDataCreate,
    PatientDataResponse,
    PatientDataUpdate,
    Token,
    APIResponse
)
from ml.predict import predict_lung_cancer_risk, get_prediction_confidence

# Create tables
Base.metadata.create_all(bind=Engine)

app = FastAPI(title="MECHA-LUNG API")

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_name = payload.get("sub")
    if user_name is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(Doctor).filter(Doctor.user_name == user_name).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get("/", response_model=APIResponse)
def read_root():
    return APIResponse(
        message="MECHA-LUNG API is running",
        status="success"
    )

@app.post("/api/doctors/register", response_model=DoctorResponse)
def register_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """Register a new doctor with encrypted password"""
    
    # Check if username already exists
    existing_user = db.query(Doctor).filter(Doctor.user_name == doctor.user_name).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new doctor
    db_doctor = Doctor(
        user_name=doctor.user_name
    )
    
    # Hash and set password
    db_doctor.set_password(doctor.password)
    
    # Save to database
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    
    return db_doctor.to_dict()

@app.post("/api/doctors/login", response_model=Token)
def login_doctor(doctor_login: DoctorLogin, db: Session = Depends(get_db)):
    """Login doctor and return access token"""
    
    # Find doctor by username
    doctor = db.query(Doctor).filter(Doctor.user_name == doctor_login.user_name).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Verify password
    if not doctor.verify_password(doctor_login.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Check if account is active
    if not doctor.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is deactivated"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": doctor.user_name}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=DoctorResponse(**doctor.to_dict())
    )

@app.get("/api/doctors/me", response_model=DoctorResponse)
def get_current_doctor_info(current_user: Doctor = Depends(get_current_user)):
    """Get current logged-in doctor information"""
    return current_user.to_dict()

@app.get("/doctors", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    """Get all doctors (admin only)"""
    doctors = db.query(Doctor).all()
    return [doctor.to_dict() for doctor in doctors]

# Patient Management Endpoints

@app.post("/api/patients", response_model=PatientDataResponse)
def create_patient(
    patient: PatientDataCreate, 
    current_user: Doctor = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new patient with ML prediction"""
    
    # Prepare data for ML prediction
    prediction_data = {
        "age": patient.age,
        "biological_gender": patient.biological_gender,
        "smoking": patient.smoking,
        "yellow_fingers": patient.yellow_fingers,
        "anxiety": patient.anxiety,
        "peer_pressure": patient.peer_pressure,
        "chronic_disease": patient.chronic_disease,
        "fatigue": patient.fatigue,
        "allergy": patient.allergy,
        "wheezing": patient.wheezing,
        "alcohol": patient.alcohol,
        "coughing": patient.coughing,
        "shortness_of_breath": patient.shortness_of_breath,
        "swallowing_difficulty": patient.swallowing_difficulty,
        "chest_pain": patient.chest_pain
    }
    
    # Get ML prediction
    lung_cancer_risk = predict_lung_cancer_risk(prediction_data)
    prediction_confidence = get_prediction_confidence(prediction_data)
    
    # Create patient record
    db_patient = PatientData(
        age=patient.age,
        biological_gender=patient.biological_gender,
        smoking=patient.smoking,
        yellow_fingers=patient.yellow_fingers,
        anxiety=patient.anxiety,
        peer_pressure=patient.peer_pressure,
        chronic_disease=patient.chronic_disease,
        fatigue=patient.fatigue,
        allergy=patient.allergy,
        wheezing=patient.wheezing,
        alcohol=patient.alcohol,
        coughing=patient.coughing,
        shortness_of_breath=patient.shortness_of_breath,
        swallowing_difficulty=patient.swallowing_difficulty,
        chest_pain=patient.chest_pain,
        lung_cancer=lung_cancer_risk,
        prediction_confidence=prediction_confidence,
        doctor_id=current_user.id
    )
    
    # Encrypt and set patient name
    db_patient.set_encrypted_name(patient.name)
    
    # Save to database
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return db_patient.to_dict()

@app.get("/api/patients", response_model=list[PatientDataResponse])
def get_patients(
    current_user: Doctor = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all patients for the current doctor"""
    patients = db.query(PatientData).filter(PatientData.doctor_id == current_user.id).all()
    return [patient.to_dict() for patient in patients]

@app.get("/api/patients/{patient_id}", response_model=PatientDataResponse)
def get_patient(
    patient_id: int,
    current_user: Doctor = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific patient by ID"""
    patient = db.query(PatientData).filter(
        PatientData.id == patient_id,
        PatientData.doctor_id == current_user.id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return patient.to_dict()

@app.put("/api/patients/{patient_id}", response_model=PatientDataResponse)
def update_patient(
    patient_id: int,
    patient_update: PatientDataUpdate,
    current_user: Doctor = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a patient's information"""
    patient = db.query(PatientData).filter(
        PatientData.id == patient_id,
        PatientData.doctor_id == current_user.id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Update fields if provided
    update_data = patient_update.dict(exclude_unset=True)
    
    # Handle name encryption separately
    if "name" in update_data:
        patient.set_encrypted_name(update_data.pop("name"))
    
    # Update other fields
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    # Re-run ML prediction if any symptoms changed
    if any(field in update_data for field in [
        "age", "biological_gender", "smoking", "yellow_fingers", "anxiety",
        "peer_pressure", "chronic_disease", "fatigue", "allergy", "wheezing",
        "alcohol", "coughing", "shortness_of_breath", "swallowing_difficulty", "chest_pain"
    ]):
        prediction_data = {
            "age": patient.age,
            "biological_gender": patient.biological_gender,
            "smoking": patient.smoking,
            "yellow_fingers": patient.yellow_fingers,
            "anxiety": patient.anxiety,
            "peer_pressure": patient.peer_pressure,
            "chronic_disease": patient.chronic_disease,
            "fatigue": patient.fatigue,
            "allergy": patient.allergy,
            "wheezing": patient.wheezing,
            "alcohol": patient.alcohol,
            "coughing": patient.coughing,
            "shortness_of_breath": patient.shortness_of_breath,
            "swallowing_difficulty": patient.swallowing_difficulty,
            "chest_pain": patient.chest_pain
        }
        
        patient.lung_cancer = predict_lung_cancer_risk(prediction_data)
        patient.prediction_confidence = get_prediction_confidence(prediction_data)
    
    db.commit()
    db.refresh(patient)
    
    return patient.to_dict()

@app.delete("/api/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    current_user: Doctor = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a patient"""
    patient = db.query(PatientData).filter(
        PatientData.id == patient_id,
        PatientData.doctor_id == current_user.id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    db.delete(patient)
    db.commit()
    
    return {"message": "Patient deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
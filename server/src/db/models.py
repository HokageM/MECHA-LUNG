from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from security import hash_password, verify_password

Base = declarative_base()

class Doctor(Base):
    __tablename__ = "doctors"
    id = mapped_column(Integer, primary_key=True, index=True)
    user_name = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String)
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    is_active = mapped_column(Boolean, default=True)
    patient_data = relationship("PatientData", back_populates="doctor")
    
    def set_password(self, password: str):
        """Hash and set the password"""
        self.hashed_password = hash_password(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify the password"""
        return verify_password(password, self.hashed_password)
    
    def to_dict(self):
        """Convert to dictionary (excluding password)"""
        return {
            "id": self.id,
            "user_name": self.user_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active
        }

class PatientData(Base):
    __tablename__ = "patient_data"
    id = mapped_column(Integer, primary_key=True, index=True)
    name_encrypted = mapped_column(String)  # Encrypted patient name
    age = mapped_column(Integer)
    biological_gender = mapped_column(Boolean)
    smoking = mapped_column(Boolean)
    yellow_fingers = mapped_column(Boolean)
    anxiety = mapped_column(Boolean)
    peer_pressure = mapped_column(Boolean)
    chronic_disease = mapped_column(Boolean)
    fatigue = mapped_column(Boolean)
    allergy = mapped_column(Boolean)
    wheezing = mapped_column(Boolean)
    alcohol = mapped_column(Boolean)
    coughing = mapped_column(Boolean)
    shortness_of_breath = mapped_column(Boolean)
    swallowing_difficulty = mapped_column(Boolean)
    chest_pain = mapped_column(Boolean)
    lung_cancer = mapped_column(Boolean)  # Set by ML prediction
    prediction_confidence = mapped_column(Float, nullable=True)  # ML confidence score
    doctor_id = mapped_column(Integer, ForeignKey("doctors.id"))
    doctor = relationship("Doctor", back_populates="patient_data")
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    
    def set_encrypted_name(self, name: str):
        """Encrypt and set patient name"""
        from encryption import encrypt_text
        self.name_encrypted = encrypt_text(name)
    
    def get_decrypted_name(self) -> str:
        """Get decrypted patient name"""
        from encryption import decrypt_text
        return decrypt_text(self.name_encrypted)
    
    def to_dict(self, include_decrypted_name: bool = True):
        """Convert to dictionary"""
        data = {
            "id": self.id,
            "age": self.age,
            "biological_gender": self.biological_gender,
            "smoking": self.smoking,
            "yellow_fingers": self.yellow_fingers,
            "anxiety": self.anxiety,
            "peer_pressure": self.peer_pressure,
            "chronic_disease": self.chronic_disease,
            "fatigue": self.fatigue,
            "allergy": self.allergy,
            "wheezing": self.wheezing,
            "alcohol": self.alcohol,
            "coughing": self.coughing,
            "shortness_of_breath": self.shortness_of_breath,
            "swallowing_difficulty": self.swallowing_difficulty,
            "chest_pain": self.chest_pain,
            "lung_cancer": self.lung_cancer,
            "prediction_confidence": self.prediction_confidence,
            "doctor_id": self.doctor_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_decrypted_name:
            data["name"] = self.get_decrypted_name()
        else:
            data["name"] = "[ENCRYPTED]"
            
        return data
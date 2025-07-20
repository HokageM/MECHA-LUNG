"""
ML prediction module for lung cancer risk assessment
"""

import joblib
import pandas as pd

model = joblib.load("server/src/ml/model/lung_cancer_model.joblib")

def convert_data(patient_data: dict) -> dict:
    """
    Convert patient data to a format that can be used by the model
    """
    return {
        "GENDER": 1 if patient_data["biological_gender"] else 0,
        "AGE": patient_data["age"],
        "SMOKING": 2 if patient_data["smoking"] else 1, 
        "YELLOW_FINGERS": 2 if patient_data["yellow_fingers"] else 1, 
        "ANXIETY": 2 if patient_data["anxiety"] else 1, 
        "PEER_PRESSURE": 2 if patient_data["peer_pressure"] else 1, 
        "CHRONIC DISEASE": 2 if patient_data["chronic_disease"] else 1, 
        "FATIGUE ": 2 if patient_data["fatigue"] else 1, 
        "ALLERGY ": 2 if patient_data["allergy"] else 1, 
        "WHEEZING": 2 if patient_data["wheezing"] else 1, 
        "ALCOHOL CONSUMING": 2 if patient_data["alcohol"] else 1, 
        "COUGHING": 2 if patient_data["coughing"] else 1, 
        "SHORTNESS OF BREATH": 2 if patient_data["shortness_of_breath"] else 1, 
        "SWALLOWING DIFFICULTY": 2 if patient_data["swallowing_difficulty"] else 1, 
        "CHEST PAIN": 2 if patient_data["chest_pain"] else 1
    }

def predict_lung_cancer_risk(patient_data: dict) -> bool:
    """
    Prediction function for lung cancer risk
    
    Args:
        patient_data: Dictionary containing patient symptoms and data
        
    Returns:
        bool: Predicted lung cancer risk (True = high risk, False = low risk)
    """
    converted_data = convert_data(patient_data)
    converted_data = pd.DataFrame([converted_data])
    return model.predict(converted_data)[0]

def get_prediction_confidence(patient_data: dict) -> float:
    """
    Mocked confidence score for the prediction
    
    Args:
        patient_data: Dictionary containing patient symptoms and data
        
    Returns:
        float: Confidence score between 0.0 and 1.0
    """
    converted_data = convert_data(patient_data)
    converted_data = pd.DataFrame([converted_data])
    return float(model.predict_proba(converted_data).max(axis=1)[0])
// API Response Types
export interface ApiData {
  message?: string;
  status?: string;
  error?: string;
}

// User/Authentication Types
export interface Doctor {
  id: number;
  user_name: string;
  created_at?: string;
  is_active: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: Doctor;
}

export interface ErrorResponse {
  detail: string;
}

// Patient Types
export interface Patient {
  id: number;
  name: string;
  age: number;
  biological_gender: boolean;
  smoking: boolean;
  yellow_fingers: boolean;
  anxiety: boolean;
  peer_pressure: boolean;
  chronic_disease: boolean;
  fatigue: boolean;
  allergy: boolean;
  wheezing: boolean;
  alcohol: boolean;
  coughing: boolean;
  shortness_of_breath: boolean;
  swallowing_difficulty: boolean;
  chest_pain: boolean;
  lung_cancer: boolean;
  prediction_confidence: number;
  created_at: string;
}

// Form Types (for creating/updating patients)
export interface PatientFormData {
  name: string;
  age: number;
  biological_gender: boolean;
  smoking: boolean;
  yellow_fingers: boolean;
  anxiety: boolean;
  peer_pressure: boolean;
  chronic_disease: boolean;
  fatigue: boolean;
  allergy: boolean;
  wheezing: boolean;
  alcohol: boolean;
  coughing: boolean;
  shortness_of_breath: boolean;
  swallowing_difficulty: boolean;
  chest_pain: boolean;
} 
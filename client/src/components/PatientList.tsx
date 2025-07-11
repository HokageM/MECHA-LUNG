import React from 'react';

interface Patient {
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

interface PatientListProps {
  patients: Patient[];
  onViewPatient: (patient: Patient) => void;
  onEditPatient: (patient: Patient) => void;
  onDeletePatient: (patientId: number) => void;
  loading?: boolean;
}

const PatientList: React.FC<PatientListProps> = ({ 
  patients, 
  onViewPatient, 
  onEditPatient,
  onDeletePatient, 
  loading = false 
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getRiskColor = (lungCancer: boolean, confidence: number) => {
    if (lungCancer) {
      return confidence > 0.8 ? '#dc3545' : '#fd7e14'; // Red for high risk, orange for medium
    }
    return confidence > 0.8 ? '#28a745' : '#ffc107'; // Green for low risk, yellow for uncertain
  };

  const getRiskLabel = (lungCancer: boolean, confidence: number) => {
    if (lungCancer) {
      return confidence > 0.8 ? 'High Risk' : 'Medium Risk';
    }
    return confidence > 0.8 ? 'Low Risk' : 'Uncertain';
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem' }}>
        <p>Loading patients...</p>
      </div>
    );
  }

  if (patients.length === 0) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '2rem',
        backgroundColor: '#f8f9fa',
        borderRadius: '8px',
        border: '1px solid #dee2e6'
      }}>
        <h3 style={{ color: '#6c757d', marginBottom: '1rem' }}>No Patients Found</h3>
        <p style={{ color: '#6c757d' }}>Add your first patient to get started.</p>
      </div>
    );
  }

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem', color: '#333' }}>Patient Records</h2>
      
      <div style={{ 
        display: 'grid', 
        gap: '1rem',
        gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))'
      }}>
        {patients.map((patient) => (
          <div key={patient.id} style={{
            backgroundColor: 'white',
            border: '1px solid #dee2e6',
            borderRadius: '8px',
            padding: '1.5rem',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}>
            {/* Header */}
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'flex-start',
              marginBottom: '1rem'
            }}>
              <div>
                <h3 style={{ margin: '0 0 0.5rem 0', color: '#333' }}>{patient.name}</h3>
                <p style={{ margin: 0, color: '#6c757d', fontSize: '0.9rem' }}>
                  Age: {patient.age} | Gender: {patient.biological_gender ? 'Male' : 'Female'}
                </p>
              </div>
              
              <div style={{
                backgroundColor: getRiskColor(patient.lung_cancer, patient.prediction_confidence),
                color: 'white',
                padding: '0.25rem 0.75rem',
                borderRadius: '20px',
                fontSize: '0.8rem',
                fontWeight: 'bold'
              }}>
                {getRiskLabel(patient.lung_cancer, patient.prediction_confidence)}
              </div>
            </div>

            {/* Risk Assessment */}
            <div style={{ 
              backgroundColor: '#f8f9fa', 
              padding: '1rem', 
              borderRadius: '4px',
              marginBottom: '1rem'
            }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#495057' }}>Risk Assessment</h4>
              <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.9rem' }}>
                <strong>Prediction:</strong> {patient.lung_cancer ? 'High Risk' : 'Low Risk'}
              </p>
              <p style={{ margin: 0, fontSize: '0.9rem' }}>
                <strong>Confidence:</strong> {(patient.prediction_confidence * 100).toFixed(1)}%
              </p>
            </div>

            {/* Key Symptoms */}
            <div style={{ marginBottom: '1rem' }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#495057' }}>Key Symptoms</h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {patient.smoking && <span style={symptomTagStyle}>Smoking</span>}
                {patient.coughing && <span style={symptomTagStyle}>Coughing</span>}
                {patient.shortness_of_breath && <span style={symptomTagStyle}>Shortness of Breath</span>}
                {patient.chest_pain && <span style={symptomTagStyle}>Chest Pain</span>}
                {patient.wheezing && <span style={symptomTagStyle}>Wheezing</span>}
                {patient.yellow_fingers && <span style={symptomTagStyle}>Yellow Fingers</span>}
                {patient.fatigue && <span style={symptomTagStyle}>Fatigue</span>}
                {patient.anxiety && <span style={symptomTagStyle}>Anxiety</span>}
                {patient.chronic_disease && <span style={symptomTagStyle}>Chronic Disease</span>}
                {patient.allergy && <span style={symptomTagStyle}>Allergy</span>}
                {patient.alcohol && <span style={symptomTagStyle}>Alcohol</span>}
                {patient.peer_pressure && <span style={symptomTagStyle}>Peer Pressure</span>}
                {patient.swallowing_difficulty && <span style={symptomTagStyle}>Swallowing Difficulty</span>}
              </div>
            </div>

            {/* Footer */}
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              borderTop: '1px solid #dee2e6',
              paddingTop: '1rem'
            }}>
              <span style={{ fontSize: '0.8rem', color: '#6c757d' }}>
                Added: {formatDate(patient.created_at)}
              </span>
              
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  onClick={() => onViewPatient(patient)}
                  style={{
                    padding: '0.5rem 1rem',
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '0.8rem'
                  }}
                >
                  View Details
                </button>
                
                <button
                  onClick={() => onEditPatient(patient)}
                  style={{
                    padding: '0.5rem 1rem',
                    backgroundColor: '#28a745',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '0.8rem'
                  }}
                >
                  Edit
                </button>
                
                <button
                  onClick={() => onDeletePatient(patient.id)}
                  style={{
                    padding: '0.5rem 1rem',
                    backgroundColor: '#dc3545',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '0.8rem'
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const symptomTagStyle = {
  backgroundColor: '#e9ecef',
  color: '#495057',
  padding: '0.25rem 0.5rem',
  borderRadius: '4px',
  fontSize: '0.75rem',
  fontWeight: '500'
};

export default PatientList; 
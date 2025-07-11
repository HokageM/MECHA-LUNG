import React, { useState } from 'react';

interface PatientFormProps {
  onSubmit: (patientData: any) => void;
  onCancel: () => void;
  loading?: boolean;
}

interface PatientData {
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

const PatientForm: React.FC<PatientFormProps> = ({ onSubmit, onCancel, loading = false }) => {
  const [formData, setFormData] = useState<PatientData>({
    name: '',
    age: 0,
    biological_gender: false,
    smoking: false,
    yellow_fingers: false,
    anxiety: false,
    peer_pressure: false,
    chronic_disease: false,
    fatigue: false,
    allergy: false,
    wheezing: false,
    alcohol: false,
    coughing: false,
    shortness_of_breath: false,
    swallowing_difficulty: false,
    chest_pain: false
  });

  const handleInputChange = (field: keyof PatientData, value: string | number | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const ToggleSwitch: React.FC<{
    label: string;
    value: boolean;
    onChange: (value: boolean) => void;
  }> = ({ label, value, onChange }) => (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center',
      marginBottom: '1rem',
      padding: '0.5rem',
      backgroundColor: '#f8f9fa',
      borderRadius: '4px'
    }}>
      <label style={{ fontWeight: '500', color: '#495057' }}>{label}</label>
      <button
        type="button"
        onClick={() => onChange(!value)}
        style={{
          width: '50px',
          height: '24px',
          backgroundColor: value ? '#28a745' : '#6c757d',
          border: 'none',
          borderRadius: '12px',
          position: 'relative',
          cursor: 'pointer',
          transition: 'background-color 0.2s'
        }}
      >
        <div style={{
          width: '20px',
          height: '20px',
          backgroundColor: 'white',
          borderRadius: '50%',
          position: 'absolute',
          top: '2px',
          left: value ? '28px' : '2px',
          transition: 'left 0.2s'
        }} />
      </button>
    </div>
  );

  return (
    <div style={{
      backgroundColor: 'white',
      padding: '2rem',
      borderRadius: '8px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      maxWidth: '600px',
      margin: '0 auto'
    }}>
      <h2 style={{ marginBottom: '1.5rem', color: '#333' }}>Add New Patient</h2>
      
      <form onSubmit={handleSubmit}>
        {/* Basic Information */}
        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ marginBottom: '1rem', color: '#495057' }}>Basic Information</h3>
          
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
              Patient Name *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }}
              required
              disabled={loading}
            />
          </div>
          
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
              Age *
            </label>
            <input
              type="number"
              value={formData.age}
              onChange={(e) => handleInputChange('age', parseInt(e.target.value) || 0)}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }}
              min="0"
              max="120"
              required
              disabled={loading}
            />
          </div>
          
          <ToggleSwitch
            label="Biological Gender (Male)"
            value={formData.biological_gender}
            onChange={(value) => handleInputChange('biological_gender', value)}
          />
        </div>

        {/* Symptoms */}
        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ marginBottom: '1rem', color: '#495057' }}>Symptoms & Risk Factors</h3>
          
          <ToggleSwitch
            label="Smoking"
            value={formData.smoking}
            onChange={(value) => handleInputChange('smoking', value)}
          />
          
          <ToggleSwitch
            label="Yellow Fingers"
            value={formData.yellow_fingers}
            onChange={(value) => handleInputChange('yellow_fingers', value)}
          />
          
          <ToggleSwitch
            label="Anxiety"
            value={formData.anxiety}
            onChange={(value) => handleInputChange('anxiety', value)}
          />
          
          <ToggleSwitch
            label="Peer Pressure"
            value={formData.peer_pressure}
            onChange={(value) => handleInputChange('peer_pressure', value)}
          />
          
          <ToggleSwitch
            label="Chronic Disease"
            value={formData.chronic_disease}
            onChange={(value) => handleInputChange('chronic_disease', value)}
          />
          
          <ToggleSwitch
            label="Fatigue"
            value={formData.fatigue}
            onChange={(value) => handleInputChange('fatigue', value)}
          />
          
          <ToggleSwitch
            label="Allergy"
            value={formData.allergy}
            onChange={(value) => handleInputChange('allergy', value)}
          />
          
          <ToggleSwitch
            label="Wheezing"
            value={formData.wheezing}
            onChange={(value) => handleInputChange('wheezing', value)}
          />
          
          <ToggleSwitch
            label="Alcohol Consumption"
            value={formData.alcohol}
            onChange={(value) => handleInputChange('alcohol', value)}
          />
          
          <ToggleSwitch
            label="Coughing"
            value={formData.coughing}
            onChange={(value) => handleInputChange('coughing', value)}
          />
          
          <ToggleSwitch
            label="Shortness of Breath"
            value={formData.shortness_of_breath}
            onChange={(value) => handleInputChange('shortness_of_breath', value)}
          />
          
          <ToggleSwitch
            label="Swallowing Difficulty"
            value={formData.swallowing_difficulty}
            onChange={(value) => handleInputChange('swallowing_difficulty', value)}
          />
          
          <ToggleSwitch
            label="Chest Pain"
            value={formData.chest_pain}
            onChange={(value) => handleInputChange('chest_pain', value)}
          />
        </div>

        {/* Buttons */}
        <div style={{ 
          display: 'flex', 
          gap: '1rem', 
          justifyContent: 'flex-end',
          borderTop: '1px solid #dee2e6',
          paddingTop: '1rem'
        }}>
          <button
            type="button"
            onClick={onCancel}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
            disabled={loading}
          >
            Cancel
          </button>
          
          <button
            type="submit"
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: loading ? '#6c757d' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
            disabled={loading}
          >
            {loading ? 'Adding Patient...' : 'Add Patient'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PatientForm; 
import React, { useState, useEffect } from 'react'
import PatientForm from './components/PatientForm'
import PatientEditForm from './components/PatientEditForm'
import PatientList from './components/PatientList'
import { 
  ApiData, 
  Doctor, 
  LoginResponse, 
  Patient,
  PatientFormData 
} from './types'
import { api } from './utils/api'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [apiData, setApiData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [loginLoading, setLoginLoading] = useState(false);
  const [currentUser, setCurrentUser] = useState<Doctor | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Patient management state
  const [patients, setPatients] = useState<Patient[]>([]);
  const [showPatientForm, setShowPatientForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [editingPatient, setEditingPatient] = useState<Patient | null>(null);
  const [patientsLoading, setPatientsLoading] = useState(false);
  const [addingPatient, setAddingPatient] = useState(false);
  const [updatingPatient, setUpdatingPatient] = useState(false);

  // Fetch API data when component mounts
  useEffect(() => {
    fetchApiData();
    checkAuthStatus();
  }, []);

  // Fetch patients when logged in
  useEffect(() => {
    if (isLoggedIn) {
      fetchPatients();
    }
  }, [isLoggedIn]);

  const fetchApiData = async () => {
    setLoading(true);
    const response = await api.publicRequest<ApiData>('/');
    if (response.data) {
      setApiData(response.data);
    } else {
      setApiData({ error: response.error || 'Failed to connect to server' });
    }
    setLoading(false);
  };

  const checkAuthStatus = () => {
    if (api.isAuthenticated()) {
      // Verify token is still valid by calling protected endpoint
      fetchCurrentUser();
    }
  };

  const fetchCurrentUser = async () => {
    const response = await api.authenticatedRequest<Doctor>('/api/doctors/me');
    if (response.data) {
      setCurrentUser(response.data);
      setIsLoggedIn(true);
    } else {
      // Token is invalid, remove it
      api.removeToken();
      setIsLoggedIn(false);
      setCurrentUser(null);
    }
  };

  const fetchPatients = async () => {
    setPatientsLoading(true);
    const response = await api.authenticatedRequest<Patient[]>('/api/patients');
    if (response.data) {
      setPatients(response.data);
    } else {
      console.error('Failed to fetch patients:', response.error);
    }
    setPatientsLoading(false);
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginLoading(true);
    setError(null);

    const response = await api.publicRequest<LoginResponse>('/api/doctors/login', {
      method: 'POST',
      body: JSON.stringify({
        user_name: username,
        password: password
      })
    });

    if (response.data) {
      // Store token
      api.setToken(response.data.access_token);
      setCurrentUser(response.data.user);
      setIsLoggedIn(true);
      setUsername('');
      setPassword('');
      setError(null);
    } else {
      setError(response.error || 'Login failed');
    }
    setLoginLoading(false);
  };

  const handleLogout = () => {
    api.removeToken();
    setIsLoggedIn(false);
    setCurrentUser(null);
    setUsername('');
    setPassword('');
    setError(null);
    setPatients([]);
    setShowPatientForm(false);
  };

  const handleAddPatient = async (patientData: PatientFormData) => {
    setAddingPatient(true);
    const response = await api.authenticatedRequest<Patient>('/api/patients', {
      method: 'POST',
      body: JSON.stringify(patientData)
    });

    if (response.data) {
      setPatients(prev => [response.data!, ...prev]);
      setShowPatientForm(false);
      alert('Patient added successfully!');
    } else {
      alert(`Failed to add patient: ${response.error}`);
    }
    setAddingPatient(false);
  };

  const handleDeletePatient = async (patientId: number) => {
    if (!confirm('Are you sure you want to delete this patient?')) {
      return;
    }

    const response = await api.authenticatedRequest(`/api/patients/${patientId}`, {
      method: 'DELETE'
    });

    if (response.status === 200) {
      setPatients(prev => prev.filter(p => p.id !== patientId));
      alert('Patient deleted successfully!');
    } else {
      alert(`Failed to delete patient: ${response.error}`);
    }
  };

  const handleViewPatient = (patient: Patient) => {
    alert(`Viewing patient: ${patient.name}\nRisk: ${patient.lung_cancer ? 'High' : 'Low'}\nConfidence: ${(patient.prediction_confidence * 100).toFixed(1)}%`);
  };

  const handleEditPatient = (patient: Patient) => {
    setEditingPatient(patient);
    setShowEditForm(true);
  };

  const handleUpdatePatient = async (patientId: number, patientData: PatientFormData) => {
    setUpdatingPatient(true);
    const response = await api.authenticatedRequest<Patient>(`/api/patients/${patientId}`, {
      method: 'PUT',
      body: JSON.stringify(patientData)
    });

    if (response.data) {
      setPatients(prev => prev.map(p => p.id === patientId ? response.data! : p));
      setShowEditForm(false);
      setEditingPatient(null);
      alert('Patient updated successfully!');
    } else {
      alert(`Failed to update patient: ${response.error}`);
    }
    setUpdatingPatient(false);
  };

  // Show login screen if not logged in
  if (!isLoggedIn) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        backgroundColor: '#f5f5f5'
      }}>
        <div style={{
          padding: '2rem',
          backgroundColor: 'white',
          borderRadius: '8px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
          width: '400px'
        }}>
          <img 
            src="/logo.jpeg" 
            alt="MECHA-LUNG Logo"  
            style={{ 
              width: '200px', 
              height: 'auto', 
              display: 'block', 
              margin: '0 auto 1rem auto',
              borderRadius: '8px'
            }} 
          />
          <h1 style={{ textAlign: 'center', color: '#333' }}>MECHA-LUNG</h1>
          <h2 style={{ textAlign: 'center', color: '#666', fontSize: '1.2rem' }}>Doctor Login</h2>
          
          {/* API Status Display */}
          <div style={{ 
            marginBottom: '1rem', 
            padding: '0.75rem', 
            backgroundColor: '#f8f9fa', 
            borderRadius: '4px',
            border: '1px solid #dee2e6'
          }}>
            <h4 style={{ margin: '0 0 0.5rem 0', color: '#495057' }}>Server Status:</h4>
            {loading ? (
              <p style={{ margin: 0, color: '#6c757d' }}>Connecting to server...</p>
            ) : apiData ? (
              <div>
                <p style={{ margin: 0, color: '#28a745', fontWeight: 'bold' }}>
                  ✅ {apiData.message}
                </p>
                <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.8rem', color: '#6c757d' }}>
                  Server is running and ready
                </p>
              </div>
            ) : (
              <p style={{ margin: 0, color: '#dc3545' }}>
                ❌ Failed to connect to server
              </p>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <div style={{ 
              marginBottom: '1rem', 
              padding: '0.75rem', 
              backgroundColor: '#f8d7da', 
              color: '#721c24',
              borderRadius: '4px',
              border: '1px solid #f5c6cb'
            }}>
              ❌ {error}
            </div>
          )}
          
          <form onSubmit={handleLogin}>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Username:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px'
                }}
                required
                disabled={loginLoading}
              />
            </div>
            
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px'
                }}
                required
                disabled={loginLoading}
              />
            </div>
            
            <button
              type="submit"
              disabled={loginLoading}
              style={{
                width: '100%',
                padding: '0.75rem',
                backgroundColor: loginLoading ? '#6c757d' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: loginLoading ? 'not-allowed' : 'pointer'
              }}
            >
              {loginLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>
          
          <p style={{ 
            textAlign: 'center', 
            marginTop: '1rem', 
            fontSize: '0.9rem', 
            color: '#666' 
          }}>
            Need an account? Contact your administrator.
          </p>
        </div>
      </div>
    );
  }

  // Show main app if logged in
  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '2rem',
        borderBottom: '1px solid #ddd',
        paddingBottom: '1rem'
      }}>
        <h1>MECHA-LUNG</h1>
        <div>
          <span style={{ marginRight: '1rem' }}>
            Welcome, Dr. {currentUser?.user_name}!
          </span>
          <button
            onClick={handleLogout}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Logout
          </button>
        </div>
      </div>
      
      <div>
        <h2>Lung Cancer Risk Prediction System</h2>
        
        {/* User Info Card */}
        <div style={{ 
          marginBottom: '2rem', 
          padding: '1rem', 
          backgroundColor: '#e7f3ff', 
          borderRadius: '8px',
          border: '1px solid #b3d9ff'
        }}>
          <h3>Doctor Information</h3>
          <p><strong>Username:</strong> {currentUser?.user_name}</p>
          <p><strong>Account Status:</strong> 
            <span style={{ 
              color: currentUser?.is_active ? '#28a745' : '#dc3545',
              fontWeight: 'bold'
            }}>
              {currentUser?.is_active ? 'Active' : 'Inactive'}
            </span>
          </p>
          {currentUser?.created_at && (
            <p><strong>Member Since:</strong> {new Date(currentUser.created_at).toLocaleDateString()}</p>
          )}
        </div>

        {/* Patient Management */}
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '1rem'
          }}>
            <h3>Patient Management</h3>
            <button
              onClick={() => setShowPatientForm(true)}
              style={{
                padding: '0.75rem 1.5rem',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              + Add New Patient
            </button>
          </div>

          {showPatientForm ? (
            <PatientForm
              onSubmit={handleAddPatient}
              onCancel={() => setShowPatientForm(false)}
              loading={addingPatient}
            />
          ) : showEditForm && editingPatient ? (
            <PatientEditForm
              patient={editingPatient}
              onSubmit={handleUpdatePatient}
              onCancel={() => {
                setShowEditForm(false);
                setEditingPatient(null);
              }}
              loading={updatingPatient}
            />
          ) : (
            <PatientList
              patients={patients}
              onViewPatient={handleViewPatient}
              onEditPatient={handleEditPatient}
              onDeletePatient={handleDeletePatient}
              loading={patientsLoading}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App 
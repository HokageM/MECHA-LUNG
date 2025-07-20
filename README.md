# MECHA-LUNG

<img src="docs/logo/logo.jpeg" alt="MECHA-LUNG Logo" width="400" height="400" />

Demo-Project: **End-to-end lung cancer risk prediction system** with secure doctor authentication, encrypted patient data, and decision-tree predictions.

## 📋 Table of Contents

1. [Overview](#overview)
3. [Architecture](#architecture)
4. [Quick Start](#quick-start)
5. [Setup Guide](#setup-guide)
6. [Authentication System](#authentication-system)
7. [Patient Data Encryption](#patient-data-encryption)
8. [API Documentation](#api-documentation)
9. [What I Learned](#what-i-learned)
10. [Technical Stack](#technical-stack)

## 🎯 Overview

MECHA-LUNG is a comprehensive healthcare application that demonstrates:

- 🔐 **Secure JWT Authentication** - Doctor login with encrypted passwords
- 🏥 **Patient Management** - Add, edit, delete, and view patient records
- 🔒 **Data Encryption** - Patient names encrypted in database
- 🤖 **ML Integration** - Automated lung cancer risk assessment
- 📊 **Risk Visualization** - Clear risk indicators and confidence scores
- 🌐 **Modern UI** - Responsive React interface
- 🛡️ **Security First** - HTTPS, CORS, and database protection

## 🏗️ Architecture

```
┌─────────────────┐    HTTPS    ┌─────────────────┐    SQL    ┌─────────────────┐
│   React Client  │ ◄─────────► │  FastAPI Server │ ◄───────► │   PostgreSQL    │
│   (Port 5173)   │             │   (Port 8000)   │           │   (Port 5432)   │
└─────────────────┘             └─────────────────┘           └─────────────────┘
         │                               │                              │
         │                               │                              │
         ▼                               ▼                              ▼
   JWT Tokens                    Lung Cancer Predictions        Fernet Encryption
   localStorage                   Mocked Model                  
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd MECHA-LUNG

# Setup Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r server/requirements.txt
cd client && npm install && cd ..
```

### 2. Database Setup
```bash
# Start PostgreSQL (if using Docker)
docker-compose up -d db

# Or use local PostgreSQL instance
# Create database: lung_db
# Create user: lung_user with password: supersecret
```

### 3. Environment Configuration
```bash
# Create server/.env file
cd server
cat > .env << 'EOF'
DATABASE_URL=postgresql://lung_user:supersecret@localhost:5432/lung_db
SECRET_KEY=your-super-secret-key-change-this-in-production-1234567890abcdef
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENCRYPTION_PASSWORD=mecha-lung-encryption-key-2024
ENCRYPTION_SALT=dV/7eHOI3szZ16tj614JNQ==
EOF
```

### 4. Database Setup
```bash
# Run complete setup script (creates tables, runs migrations, creates sample doctor)
python setup.py
```

### 5. Start Services
```bash
# Terminal 1: Start FastAPI server
python src/main.py

# Terminal 2: Start React client
cd ../client
npm run dev
```

### 6. Access Application
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Login**: Use the sample account created by setup.py (dr_naruto / hokage)

## 📸 Application Screenshots

### Login Screen
![Login Screen](docs/screenshots/LoginScreen.png)
*Secure doctor authentication with JWT token management*

### Dashboard
![Dashboard](docs/screenshots/Dashoard.png)
*Main application interface with patient management and risk assessment*

### Patient Creation
![Patient Creation](docs/screenshots/PatientCreation.png)
*Adding new patients with encrypted name storage and automated risk prediction*

## 🔧 Setup Guide

### Database Configuration

#### Docker
```yaml
# docker-compose.yml
version: "3.9"
services:
  db:
    image: postgres
    container_name: mecha_lung_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: lung_db
      POSTGRES_USER: lung_user
      POSTGRES_PASSWORD: supersecret
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
volumes:
  pg_data:
```

### Environment Variables

**Required for server/.env:**
```bash
# Database
DATABASE_URL=postgresql://lung_user:supersecret@localhost:5432/lung_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-1234567890abcdef
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Encryption (DO NOT CHANGE AFTER SETUP)
ENCRYPTION_PASSWORD=mecha-lung-encryption-key-2024
ENCRYPTION_SALT=dV/7eHOI3szZ16tj614JNQ==
```

## 🔐 Authentication System

### JWT Token Workflow

#### 1. **Doctor Registration**
```bash
POST /api/doctors/register
{
  "user_name": "dr_naruto",
  "password": "hokage"
}
```

#### 2. **Doctor Login**
```bash
POST /api/doctors/login
{
  "user_name": "dr_naruto", 
  "password": "hokage"
}

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "user_name": "dr_naruto",
    "is_active": true
  }
}
```

#### 3. **Token Usage**
```bash
# Include in API requests
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: 30-minute expiration
- **Stateless Authentication**: No server-side sessions
- **Token Validation**: Automatic verification on protected endpoints

## 🔒 Patient Data Encryption

### Overview

Patient names are encrypted using **Fernet symmetric encryption** (AES-128) before storage in the database.

### Encryption Flow

```
1. Doctor enters: "Naruto Uzumaki"
2. Server encrypts: "Naruto Uzumaki" → "Z0FBQUFBQm9j..."
3. Database stores: "Z0FBQUFBQm9j..."
4. Server retrieves: "Z0FBQUFBQm9j..."
5. Server decrypts: "Z0FBQUFBQm9j..." → "Naruto Uzumaki"
6. Client displays: "Naruto Uzumaki"
```

### Technical Implementation

**Key Generation:**
```python
def get_encryption_key() -> bytes:
    password = settings.ENCRYPTION_PASSWORD
    salt = settings.ENCRYPTION_SALT
    key, _ = generate_key_from_password(password, base64.b64decode(salt))
    return key
```

**Database Model:**
```python
class PatientData(Base):
    name_encrypted = mapped_column(String)
    
    def set_encrypted_name(self, name: str):
        self.name_encrypted = encrypt_text(name)
    
    def get_decrypted_name(self) -> str:
        return decrypt_text(self.name_encrypted)
```

### Security Benefits

- **Database Breach Protection**: Encrypted names remain unreadable
- **Transparent to Users**: Doctors see readable names in interface

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/doctors/register` | Register new doctor |
| POST | `/api/doctors/login` | Doctor login |
| GET | `/api/doctors/me` | Get current doctor info |

### Patient Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/patients` | Create new patient |
| GET | `/api/patients` | Get all patients |
| GET | `/api/patients/{id}` | Get specific patient |
| PUT | `/api/patients/{id}` | Update patient |
| DELETE | `/api/patients/{id}` | Delete patient |

### Example API Usage

**Create Patient:**
```bash
curl -X POST "http://localhost:8000/api/patients" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Saske Uchiha",
    "age": 19,
    "smoking": true,
    "coughing": true,
    "shortness_of_breath": false
  }'
```

**Get Patients:**
```bash
curl -X GET "http://localhost:8000/api/patients" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🎓 What I Learned

### 1. **Authentication & Security**

**JWT Implementation:**
- Learned how JWT tokens work (header, payload, signature)
- Implemented stateless authentication system
- Understood token expiration and refresh strategies

**Password Hashing**
- Practiced secure password hashing with bcrypt

**Key Concepts:**
- **Stateless vs Stateful**: JWT eliminates server-side sessions
- **Token Security**: Tamper-proof through cryptographic signatures
- **Password Security**: Hashing vs encryption for different use cases

### 2. **Database Design & Security**

**Encryption Implementation:**
- Implemented field-level encryption for sensitive data
- Understood salt importance for consistent encryption

**Database Concepts:**
- **ORM Usage**: SQLAlchemy for database operations
- **Migration Strategies**: Safe schema updates without data loss
- **Relationship Modeling**: Doctor-Patient relationships

### 3. **API Development**

**FastAPI Framework:**
- Built RESTful APIs with automatic documentation
- Implemented dependency injection for authentication
- Learned request/response modeling with Pydantic

**API Design Patterns:**
- **CRUD Operations**: Complete patient management
- **Authentication**: JWT token verification
- **CORS Configuration**: Cross-origin request handling

### 4. **Frontend Development**

**React with TypeScript:**
- Built responsive UI components
- Implemented state management for forms

**User Experience:**
- **Toggle Switches**: Intuitive boolean input controls
- **Loading States**: User feedback during operations
- **Error Handling**: Graceful error display
- **Responsive Design**: Mobile-friendly interface

### 5. Handling Unbalanced Datasets

Dealing with class imbalance is crucial for building robust machine learning models, especially in this [medical dataset](https://www.kaggle.com/datasets/mysarahmadbhat/lung-cancer) where negative cases (e.g., cancer) are rare.

- **Stratified Split:**  
  Ensures both training and test sets maintain the original class distribution, preventing bias during evaluation.

- **Balanced Accuracy Score:**  
  - Defined as the arithmetic mean of sensitivity (recall for the positive class) and specificity (recall for the negative class).
  - For binary classification, this is equivalent to the ROC-AUC score.
  - Provides a more informative metric than plain accuracy on imbalanced data.

- **SMOTE (Synthetic Minority Over-sampling Technique):**  
  - Generates artificial examples of the minority class to balance the dataset.
  - Applied only to the training data to prevent data leakage.

**How SMOTE Works:**
1. Select a minority-class sample \( x \).
2. Find its \( k \) nearest minority-class neighbors.
3. Randomly choose one of these neighbors \( x_n \).
4. Synthesize a new sample along the line segment between \( x \) and \( x_n \).
5. Repeat until the desired number of synthetic samples is reached.

## 🛠️ Technical Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **Encryption**: cryptography (Fernet)
- **Password Hashing**: bcrypt
- **Server**: uvicorn

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Inline styles
- **HTTP Client**: Fetch API

### Security
- **Authentication**: JWT tokens
- **Encryption**: AES-128 (Fernet)
- **Password Security**: bcrypt hashing
- **Transport**: HTTPS/TLS
- **CORS**: Cross-origin resource sharing

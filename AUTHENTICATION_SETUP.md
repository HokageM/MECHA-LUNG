# MECHA-LUNG Authentication Setup Guide

This guide explains how to set up and test the JWT-based authentication system.

## Prerequisites

1. **Database**: PostgreSQL running with the MECHA-LUNG database
2. **Python Dependencies**: All required packages installed
3. **React App**: Client application ready to run

## Setup Steps

### 1. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 2. Run Database Migration

```bash
cd server/src
python migrate_db.py
```

This will:
- Check if the `doctors` table exists
- Add missing columns (`created_at`, `is_active`)
- Create tables if they don't exist

### 3. Add a Doctor Account

```bash
cd server/src
python add_doctor.py
```

Follow the prompts to create a doctor account:
- Enter username (e.g., `dr_smith`)
- Enter password (e.g., `securepass123`)

### 4. Start the FastAPI Server

```bash
cd server/src
python main.py
```

The server will start on `http://localhost:8000`

### 5. Start the React App

```bash
cd client
npm run dev
```

The app will start on `http://localhost:5173`

## Testing the Authentication

### 1. Login Flow

1. Open `http://localhost:5173` in your browser
2. You should see the login screen with server status
3. Enter the credentials you created with `add_doctor.py`
4. Click "Login"
5. If successful, you'll be redirected to the dashboard

### 2. API Endpoints

#### Public Endpoints (No Auth Required)
- `GET /` - Server status
- `POST /api/doctors/register` - Register new doctor
- `POST /api/doctors/login` - Login

#### Protected Endpoints (Auth Required)
- `GET /api/doctors/me` - Get current user info
- `GET /doctors` - Get all doctors (admin)

### 3. Testing with curl

#### Login
```bash
curl -X POST "http://localhost:8000/api/doctors/login" \
     -H "Content-Type: application/json" \
     -d '{"user_name": "dr_smith", "password": "securepass123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "user_name": "dr_smith",
    "created_at": "2024-01-15T10:30:00",
    "is_active": true
  }
}
```

#### Get Current User (Protected)
```bash
curl -X GET "http://localhost:8000/api/doctors/me" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. JWT Token Details

The JWT token contains:
- **Header**: Algorithm info (HS256)
- **Payload**: User data and expiration
- **Signature**: Verification hash

Token structure:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkcl9zbWl0aCIsImV4cCI6MTczNDU2NzgwMH0.signature
```

## Security Features

### 1. Password Hashing
- Passwords are hashed using bcrypt
- Each password gets a unique salt
- Cannot be reversed or decrypted

### 2. JWT Tokens
- Tokens expire after 30 minutes (configurable)
- Signed with a secret key
- Cannot be tampered with

### 3. CORS Protection
- Only allows requests from specified origins
- Prevents cross-origin attacks

## Troubleshooting

### Common Issues

1. **"Failed to connect to server"**
   - Make sure FastAPI server is running
   - Check if port 8000 is available

2. **"Invalid credentials"**
   - Verify username and password
   - Check if doctor account exists in database

3. **"Token expired"**
   - Login again to get a new token
   - Tokens expire after 30 minutes

4. **Database connection errors**
   - Ensure PostgreSQL is running
   - Check database credentials in `config.py`

### Debug Mode

To see detailed error messages, check the browser console and server logs.

## Production Considerations

1. **Change Secret Key**: Update `SECRET_KEY` in production
2. **HTTPS**: Use HTTPS in production
3. **Token Expiration**: Adjust token expiration time
4. **Rate Limiting**: Add rate limiting for login attempts
5. **Password Policy**: Implement strong password requirements


## Next Steps

1. Add patient data management
2. Implement role-based access control
3. Add password reset functionality
4. Implement session management
5. Add audit logging 
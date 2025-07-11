#!/usr/bin/env python3
"""
Script to add a doctor to the database with encrypted password
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.database import SessionLocal
from db.models import Doctor

def add_doctor(username: str, password: str):
    """Add a new doctor to the database"""
    
    db = SessionLocal()
    try:
        # Check if doctor already exists
        existing_doctor = db.query(Doctor).filter(Doctor.user_name == username).first()
        if existing_doctor:
            print(f"❌ Doctor with username '{username}' already exists!")
            return False
        
        # Create new doctor
        doctor = Doctor(
            user_name=username
        )
        
        # Hash and set password
        doctor.set_password(password)
        
        # Save to database
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        
        print(f"✅ Doctor '{username}' added successfully!")
        print(f"   Username: {username}")
        print(f"   Password: {'*' * len(password)} (encrypted)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding doctor: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    print("🏥 MECHA-LUNG Doctor Registration")
    print("=" * 40)
    
    # Get input from user
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    # Validate input
    if not all([username, password]):
        print("❌ All fields are required!")
        return
    
    # Add doctor
    success = add_doctor(username, password)
    
    if success:
        print("\n🎉 Doctor registered successfully!")
        print("You can now login with these credentials.")
    else:
        print("\n💥 Registration failed!")

if __name__ == "__main__":
    main() 
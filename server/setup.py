#!/usr/bin/env python3
"""
Complete setup script for MECHA-LUNG
Creates tables, runs migrations, and sets up the database
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text, inspect
from config import settings
from db.database import Engine
from db.models import Base

def setup_database():
    """Complete database setup"""
    
    print("🔄 Setting up MECHA-LUNG database...")
    
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please ensure PostgreSQL is running and DATABASE_URL is correct")
        return False
    
    # Create all tables
    print("📋 Creating database tables...")
    try:
        Base.metadata.create_all(bind=Engine)
        print("✅ All tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    # Check if patient_data table exists and has required columns
    inspector = inspect(engine)
    if 'patient_data' in inspector.get_table_names():
        existing_columns = [col['name'] for col in inspector.get_columns('patient_data')]
        print(f"📊 Patient data table columns: {existing_columns}")
        
        # Check for required columns
        required_columns = ['age', 'prediction_confidence']
        missing_columns = [col for col in required_columns if col not in existing_columns]
        
        if missing_columns:
            print(f"🔧 Adding missing columns: {missing_columns}")
            with engine.connect() as conn:
                for col_name in missing_columns:
                    try:
                        if col_name == 'age':
                            sql = "ALTER TABLE patient_data ADD COLUMN age INTEGER DEFAULT 0"
                        elif col_name == 'prediction_confidence':
                            sql = "ALTER TABLE patient_data ADD COLUMN prediction_confidence FLOAT"
                        
                        conn.execute(text(sql))
                        conn.commit()
                        print(f"✅ Added column: {col_name}")
                    except Exception as e:
                        print(f"❌ Error adding column {col_name}: {e}")
                        return False
        else:
            print("✅ All required columns already exist")
    
    print("🎉 Database setup completed successfully!")
    return True

def create_sample_doctor():
    """Create a sample doctor account"""
    
    print("\n👨‍⚕️ Creating sample doctor account...")
    
    try:
        from db.database import SessionLocal
        from db.models import Doctor
        from security import hash_password
        
        db = SessionLocal()
        
        # Check if doctor already exists
        existing_doctor = db.query(Doctor).filter(Doctor.user_name == "dr_naruto").first()
        if existing_doctor:
            print("✅ Sample doctor 'dr_naruto' already exists")
            db.close()
            return True
        
        # Create sample doctor
        doctor = Doctor(
            user_name="dr_naruto"
        )
        doctor.set_password("hokage")
        
        db.add(doctor)
        db.commit()
        db.close()
        
        print("✅ Sample doctor created successfully!")
        print("   Username: dr_naruto")
        print("   Password: hokage")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample doctor: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🚀 MECHA-LUNG Setup Script")
    print("=" * 50)
    
    # Check environment variables
    if not settings.DATABASE_URL:
        print("❌ DATABASE_URL not set. Please check your .env file")
        return False
    
    if not settings.ENCRYPTION_SALT:
        print("❌ ENCRYPTION_SALT not set. Please check your .env file")
        return False
    
    print("✅ Environment variables configured")
    
    # Setup database
    if not setup_database():
        return False
    
    # Create sample doctor
    if not create_sample_doctor():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the server: python src/main.py")
    print("2. Start the client: cd ../client && npm run dev")
    print("3. Login with: dr_naruto / hokage")
    print("4. Access the app at: http://localhost:5173")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1) 
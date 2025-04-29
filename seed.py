# seed.py
from app import create_app, db
from app.models.db_models import Patient
from datetime import datetime

# Create the app
app = create_app()

# Function to add sample data
def seed_data():
    # Make sure we don't add duplicates if patients already exist
    if Patient.query.count() == 0:
        patients = [
            Patient(
                patient_id="P001",
                name="John Doe",
                age=30,
                gender="Male",
                phone="123-456-7890",
                symptoms="Headache, nausea",
                registration_date=datetime(2025, 3, 16, 10, 0, 0)  # Specific date for testing
            ),
            Patient(
                patient_id="P002",
                name="Jane Smith",
                age=25,
                gender="Female",
                phone="234-567-8901",
                symptoms="Dizziness, blurred vision",
                registration_date=datetime(2025, 3, 16, 12, 30, 0)
            ),
            Patient(
                patient_id="P003",
                name="Alice Johnson",
                age=40,
                gender="Female",
                phone="345-678-9012",
                symptoms="Severe headache, fatigue",
                registration_date=datetime(2025, 3, 15, 9, 15, 0)
            ),
            Patient(
                patient_id="P004",
                name="Bob Brown",
                age=50,
                gender="Male",
                phone="456-789-0123",
                symptoms="Memory loss, confusion",
                registration_date=datetime(2025, 3, 14, 15, 45, 0)
            ),
        ]

        # Add the patients to the database
        db.session.add_all(patients)
        db.session.commit()
        print("Data seeded successfully.")
    else:
        print("Data already seeded.")

# Run the script within the app context
with app.app_context():
    seed_data()

from app_sqlite import app, db
from app_sqlite import Client  # Import your model

# Create sample data
seed_data = [
    Client(name="Alice Johnson", email="alice@example.com"),
    Client(name="Bob Smith", email="bob@example.com"),
    Client(name="Charlie Brown", email="charlie@example.com")
]

# Function to seed the database
def seed_database():
    with app.app_context():  # Ensure we are in the Flask application context
        db.create_all()  # Create tables if they don't exist
        db.session.bulk_save_objects(seed_data)  # Insert multiple records
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()

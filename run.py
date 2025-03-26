from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

#print(os.environ)  

# Read and print environment variable
db_password = os.getenv('DB_PASSWORD')
print(f"DB_PASSWORD: {db_password}")  # Ensure it's printed


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} - {rule.endpoint}")
    

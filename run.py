from app import create_app
import os
from dotenv import load_dotenv
import time
import webbrowser
import threading

# Load environment variables first
load_dotenv()

# Read and print environment variable
db_password = os.getenv('DB_PASSWORD')
print(f"DB_PASSWORD: {db_password}")  # Ensure it's printed

# Initialize Flask app
app = create_app()

# Function to open the default browser automatically after server starts
def open_browser():
    # Give the server some time to start
    time.sleep(3)
    url = "http://0.0.0.0:5001/api/patients/form"  # Your form URL
    webbrowser.open(url, new=2)  # new=2 opens it in a new tab

# Start the browser-opening function in a separate thread to avoid blocking the server
threading.Thread(target=open_browser).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} - {rule.endpoint}")

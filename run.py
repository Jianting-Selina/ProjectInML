from app import create_app
import os
from dotenv import load_dotenv
import time
import webbrowser
import threading

# Load environment variables first
load_dotenv()

# Read and print environment variable
DOCKER_PORT = os.getenv('DOCKER_PORT')
print(f"DOCKER_PORT: {DOCKER_PORT}")  # Ensure it's printed

# Initialize Flask app
app = create_app()

# Function to open the default browser automatically after server starts
def open_browser():
    # Give the server some time to start
    time.sleep(3)
    url = "http://0.0.0.0:5001/api/patients/form"  # Your form URL
    webbrowser.open(url, new=2)  # new=2 opens it in a new tab




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=DOCKER_PORT, debug=True)

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} - {rule.endpoint}")

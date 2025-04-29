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
    url = f"http://0.0.0.0:{DOCKER_PORT}/api/patients/form"  # Your form URL
    webbrowser.open(url, new=2)  # new=2 opens it in a new tab

if __name__ == "__main__":
    # Only open browser in the main process, not in the reloader
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Thread(target=open_browser).start()
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=int(DOCKER_PORT) if DOCKER_PORT else 5001, debug=True)

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} - {rule.endpoint}")
import os
import subprocess
import webbrowser
from threading import Thread
import time

# Step 1: Run model.py to generate the forecast and original JSON files
def run_model():
    print("Generating data with model.py...")
    subprocess.run(['python', 'model.py'])
    print("Data generated successfully.")

# Step 2: Start the Flask API from app.py
def run_flask_app():
    print("Starting Flask server with app.py...")
    subprocess.run(['python', 'app.py'])  # This will run app.py in a separate process

# Step 3: Open the index.html (served by Flask) in the default web browser
def open_browser():
    url = 'http://127.0.0.1:5000/'  # Opening the index.html served by Flask
    print(f"Opening browser to {url}...")
    time.sleep(3)  # Give the Flask app some time to start before opening the browser
    webbrowser.open(url)

if __name__ == "__main__":
    # Step 1: Run the model to generate the data
    run_model()

    # Step 2: Run Flask in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    # Step 3: Open the frontend in the browser
    open_browser()

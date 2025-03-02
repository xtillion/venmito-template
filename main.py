""" # main.py

# ... (any other imports or code you have in main.py) ...

if __name__ == "__main__":
    # When main.py is run, start the FastAPI server by running server.py
    import subprocess
    import sys
    subprocess.run([sys.executable, "server.py"])
 """

import os
import subprocess
import time

# Get base directory (adjust if needed)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths to scripts
SETUP_DB_SCRIPT = os.path.join(BASE_DIR, "src/database/setup_db.py")
INGEST_SCRIPTS = [
    os.path.join(BASE_DIR, "src/ingestions/ingest_people.py"),
    os.path.join(BASE_DIR, "src/ingestions/ingest_transactions.py"),
    os.path.join(BASE_DIR, "src/ingestions/ingest_transfers.py"),
    os.path.join(BASE_DIR, "src/ingestions/ingest_promotions.py")
]
API_SERVER_SCRIPT = os.path.join(BASE_DIR, "server.py")

# ✅ Step 1: Run setup_db.py
print("🔄 Setting up database...")
subprocess.run(["python", SETUP_DB_SCRIPT], check=True)

# ✅ Step 2: Run all ingestion scripts
print("🔄 Running ingestion scripts...")
for script in INGEST_SCRIPTS:
    print(f"➡️ Running {script} ...")
    subprocess.run(["python", script], check=True)

# ✅ Step 3: Start the FastAPI server
print("🚀 Starting FastAPI Server...")
api_process = subprocess.Popen(["python", API_SERVER_SCRIPT])

# ✅ Step 4: Launch Jupyter Notebook Server
print("📝 Launching Jupyter Notebook...")
jupyter_process = subprocess.Popen(["jupyter", "notebook"], cwd=os.path.join(BASE_DIR, "notebooks"))

# Keep processes running
try:
    api_process.wait()
    jupyter_process.wait()
except KeyboardInterrupt:
    print("🛑 Stopping services...")
    api_process.terminate()
    jupyter_process.terminate()

# main.py

# ... (any other imports or code you have in main.py) ...

if __name__ == "__main__":
    # When main.py is run, start the FastAPI server by running server.py
    import subprocess
    import sys
    subprocess.run([sys.executable, "server.py"])

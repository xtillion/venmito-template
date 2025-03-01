import os
import subprocess
import sys

import uvicorn

from src.api.Router import app  # Import FastAPI app instance from Router.py

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

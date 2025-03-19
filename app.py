"""Main Flask application."""

from flask import Flask, render_template
from src.api.routes import register_routes

app = Flask(__name__)

# Register API routes
register_routes(app)

@app.route("/")
def index():
    """Render the main dashboard."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

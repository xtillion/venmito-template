from flask import Flask, jsonify, render_template
from flask_cors import CORS
from scripts.database import save_to_db
from scripts.analysis import get_clients_with_promotions, get_top_stores, get_top_transfers, get_store_sales_past_year, get_avg_transaction_value, get_promotion_analysis, get_revenue_trend, get_transaction_distribution, get_top_customers, get_customer_data, get_transactions_data, get_earnings_data, get_earnings_trends
from scripts.database import query_db
import pandas as pd
from flask import send_file

# ✅ Initialize Flask App
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ✅ Refresh Data
save_to_db()

# ✅ Serve the Homepage
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/earnings")
def earnings():
    return render_template("earnings.html")

@app.route("/transactions")
def transactions():
    return render_template("transactions.html")

@app.route("/customers")
def customers():
    return render_template("customers.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/help")
def help():
    return render_template("help.html")


# ✅ API Routes
@app.route("/clients/promotions", methods=["GET"])
def clients_promotions():
    return jsonify(get_clients_with_promotions().to_dict(orient="records"))

@app.route("/stores/top", methods=["GET"])
def top_stores():
    return jsonify(get_top_stores().to_dict(orient="records"))

@app.route("/stores/sales", methods=["GET"])
def store_sales():
    return jsonify(get_store_sales_past_year().to_dict(orient="records"))

@app.route("/clients/top-transfers", methods=["GET"])
def top_transfers():
    return jsonify(get_top_transfers().to_dict(orient="records"))

@app.route("/earnings/avg-transaction", methods=["GET"])
def avg_transaction():
    result = get_avg_transaction_value()
    return jsonify(result.to_dict(orient="records"))

# Analytics API Routes
@app.route("/analytics/revenue-trend", methods=["GET"])
def revenue_trend():
    return jsonify(get_revenue_trend().to_dict(orient="records"))

@app.route("/analytics/transaction-distribution", methods=["GET"])
def transaction_distribution():
    return jsonify(get_transaction_distribution().to_dict(orient="records"))

# Customers API Routes
@app.route("/customers/top", methods=["GET"])
def top_customers():
    return jsonify(get_top_customers().to_dict(orient="records"))

@app.route("/customers/data", methods=["GET"])
def customer_data():
    return jsonify(get_customer_data().to_dict(orient="records"))

# Transactions API Route
@app.route("/transactions/data", methods=["GET"])
def transactions_data():
    return jsonify(get_transactions_data().to_dict(orient="records"))

# Earnings API Routes
@app.route("/earnings/data", methods=["GET"])
def earnings_data():
    return jsonify(get_earnings_data().to_dict(orient="records"))

@app.route("/earnings/trends", methods=["GET"])
def earnings_trends():
    return jsonify(get_earnings_trends().to_dict(orient="records"))

@app.route("/clients/promotions-analysis", methods=["GET"])
def promotions_analysis():
    return jsonify(get_promotion_analysis().to_dict(orient="records"))

# Route to serve the CSV file
@app.route("/download-csv")
def download_csv():
    df = pd.read_csv("data/cleaned_client_data.csv")  # Load your cleaned data
    df.to_csv("data/download.csv", index=False)  # Save a new file

    return send_file("data/download.csv", as_attachment=True)

# ✅ Run the API
if __name__ == "__main__":
    app.run(debug=True)
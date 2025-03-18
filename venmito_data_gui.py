import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_data(query, params=()):
    """Fetch data from the database based on a query."""
    conn = sqlite3.connect("venmito_master.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

def show_promotion_data():
    """Display which clients have what type of promotion."""
    query = "SELECT name, email, phone_number, promoted_item FROM venmito_data WHERE promoted_item IS NOT NULL"
    data = fetch_data(query)
    messagebox.showinfo("Promotion Data", "\n".join([f"{row[0]} ({row[1]}) - {row[3]}" for row in data]))

def suggest_promotion_improvements():
    """Provide suggestions to turn "No" responses into "Yes" for promotions."""
    query = "SELECT name, email, phone_number FROM venmito_data WHERE responded = 'No'"
    data = fetch_data(query)
    messagebox.showinfo("Promotion Improvement Suggestions", "These clients have not responded:\n\n" + "\n".join([f"{row[0]} ({row[1]})" for row in data]))

def best_selling_items():
    """Determine the best-selling items, ignoring blank spaces."""
    query = "SELECT purchased_item, COUNT(*) AS count FROM venmito_data WHERE purchased_item IS NOT NULL AND purchased_item != '' GROUP BY purchased_item ORDER BY count DESC LIMIT 5"
    data = fetch_data(query)
    messagebox.showinfo("Best-Selling Items", "\n".join([f"{row[0]} - {row[1]} sales" for row in data]))

def most_profitable_stores():
    """Find the store with the highest total sales."""
    query = "SELECT store, SUM(price) as total_revenue FROM venmito_data GROUP BY store ORDER BY total_revenue DESC LIMIT 5"
    data = fetch_data(query)
    messagebox.showinfo("Most Profitable Stores", "\n".join([f"{row[0]} - ${row[1]:.2f}" for row in data]))

def visualize_transfers():
    """Generate a visualization for top senders in transfers."""
    query = "SELECT sent_from, SUM(amount_sent) FROM venmito_data WHERE sent_from IS NOT NULL GROUP BY sent_from ORDER BY SUM(amount_sent) DESC LIMIT 10"
    data = fetch_data(query)
    
    if not data:
        messagebox.showwarning("Visualization", "No transfer data available.")
        return
    
    labels, values = zip(*data)
    
    # Create a larger figure size
    fig, ax = plt.subplots(figsize=(10, 6))  # Increased figure size
    
    ax.bar(labels, values, color='blue')
    ax.set_title("Top Senders in Transfers", fontsize=14)
    ax.set_xlabel("Sender ID", fontsize=12)
    ax.set_ylabel("Total Amount Sent", fontsize=12)
    
    # Rotate x-axis labels and adjust layout to prevent cut-off
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=10)
    
    fig.tight_layout()  # Ensures the labels fit within the frame
    
    # Display the updated plot
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def handle_query():
    """Execute the function based on dropdown selection."""
    selected_query = query_var.get()
    if selected_query == questions[0]:
        show_promotion_data()
    elif selected_query == questions[1]:
        suggest_promotion_improvements()
    elif selected_query == questions[2]:
        best_selling_items()
    elif selected_query == questions[3]:
        most_profitable_stores()
    elif selected_query == questions[4]:
        visualize_transfers()

def create_gui():
    """Create the main GUI window."""
    global window, query_var
    window = tk.Tk()
    window.title("Venmito Data Explorer")
    window.geometry("600x400")
    
    tk.Label(window, text="Select a question:", font=("Arial", 12)).pack(pady=10)
    
    query_var = tk.StringVar()
    dropdown = ttk.Combobox(window, textvariable=query_var, values=questions, width=80)  # Increased width
    dropdown.pack()
    dropdown.current(0)
    
    tk.Button(window, text="Run Query", command=handle_query, font=("Arial", 12)).pack(pady=20)
    
    window.mainloop()

questions = [
    "Which clients have what type of promotion?",
    "Give suggestions on how to turn 'No' responses from clients in the promotions file.",
    "What item is the best seller?",
    "What store has had the most profit?",
    "How can we use the data we got from the transfer file?"
]

if __name__ == "__main__":
    create_gui()

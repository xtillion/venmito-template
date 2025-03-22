import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class GUIHandler:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.window = tk.Tk()
        self.window.title("Venmito Data Analysis")
        self.window.geometry("800x600")

        # Title Label
        title = tk.Label(self.window, text="Venmito Data Analysis", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # Create Button Frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)

        # Create Buttons
        buttons = [
            ("Top Clients", self.show_top_clients),
            ("Most Profitable Store", self.show_top_stores),
            ("Promotion Suggestions", self.show_promotion_suggestions),
            ("Top Senders", self.show_top_senders),
            ("Top Recipients", self.show_top_recipients),
            ("Unusual Transfers", self.show_unusual_transfers),
            ("Most Valuable Clients (VIP)", self.show_most_valuable_clients),
            ("Location-Based Spending", self.show_location_patterns),
            ("Avg Transaction per Store", self.show_average_transaction_value),
            ("Most Common Transfer Amount", self.show_most_common_transfer_amount),
            ("Store Customer Count", self.show_store_customers),
            ("Most Popular Store for Items", self.show_most_popular_store_for_items),
            ("Transfer Pattern by Day", self.show_transfer_pattern_by_day)
        ]

        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command, width=30)
            btn.pack(side="top", pady=2)

        # Table Display
        self.table = ttk.Treeview(self.window)
        self.table.pack(expand=True, fill="both", pady=10)

        self.window.mainloop()

    def display_table(self, data):
        # Clear previous table
        for row in self.table.get_children():
            self.table.delete(row)

        if isinstance(data, pd.DataFrame):
            self.table["columns"] = list(data.columns)
            self.table["show"] = "headings"

            for col in data.columns:
                self.table.heading(col, text=col)

            for _, row in data.iterrows():
                self.table.insert("", "end", values=list(row))

        else:
            messagebox.showinfo("Info", data)

    def show_top_clients(self):
        data = self.analyzer.get_top_clients()
        self.display_table(data)

    def show_top_stores(self):
        data = self.analyzer.get_top_stores()
        self.display_table(data)

    def show_promotion_suggestions(self):
        data = self.analyzer.get_promotion_suggestions()
        self.display_table(data)

    def show_top_senders(self):
        data = self.analyzer.get_top_senders()
        self.display_table(data)

    def show_top_recipients(self):
        data = self.analyzer.get_top_recipients()
        self.display_table(data)

    def show_unusual_transfers(self):
        data = self.analyzer.get_unusual_transfers()
        self.display_table(data)

    def show_most_valuable_clients(self):
        data = self.analyzer.get_most_valuable_clients()
        self.display_table(data)

    def show_location_patterns(self):
        data = self.analyzer.get_location_patterns()
        self.display_table(data)

    def show_average_transaction_value(self):
        data = self.analyzer.get_average_transaction_value()
        self.display_table(data)

    def show_most_common_transfer_amount(self):
        data = self.analyzer.get_most_common_transfer_amount()
        messagebox.showinfo("Most Common Transfer Amount", data)

    def show_store_customers(self):
        data = self.analyzer.get_store_customers()
        self.display_table(data)

    def show_most_popular_store_for_items(self):
        data = self.analyzer.get_most_popular_store_for_items()
        self.display_table(data)

    def show_transfer_pattern_by_day(self):
        data = self.analyzer.get_transfer_pattern_by_day()
        self.display_table(data)

# Example usage:
# from analysis import DataAnalyzer
# analyzer = DataAnalyzer(people_df, transactions_df, transfers_df, promotions_df)
# GUIHandler(analyzer)

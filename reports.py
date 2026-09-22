import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


def get_transactions():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            st.transaction_id,
            p.product_name,
            st.transaction_type,
            st.quantity,
            st.transaction_date
        FROM stock_transactions st
        JOIN products p
            ON st.product_id = p.product_id
        ORDER BY st.transaction_date DESC
    """

    cursor.execute(query)
    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions

class ReportsWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("StockFlow - Reports")
        self.window.geometry("850x500")
        self.window.resizable(False, False)

        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):

        title = tk.Label(
            self.window,
            text="TRANSACTION HISTORY",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        # Refresh button
        tk.Button(
            self.window,
            text="REFRESH",
            width=15,
            command=self.load_transactions
        ).pack(pady=5)

        # Table
        columns = (
            "ID",
            "Product",
            "Type",
            "Quantity",
            "Date"
        )

        self.table = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            height=17
        )

        self.table.heading("ID", text="Transaction ID")
        self.table.heading("Product", text="Product")
        self.table.heading("Type", text="Type")
        self.table.heading("Quantity", text="Quantity")
        self.table.heading("Date", text="Date & Time")

        self.table.column("ID", width=100)
        self.table.column("Product", width=250)
        self.table.column("Type", width=100)
        self.table.column("Quantity", width=100)
        self.table.column("Date", width=200)

        self.table.pack(
            padx=20,
            pady=10
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.window,
            orient="vertical",
            command=self.table.yview
        )

        scrollbar.place(
            x=810,
            y=95,
            height=365
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

    def load_transactions(self):

        try:
            transactions = get_transactions()

            # Clear table
            for item in self.table.get_children():
                self.table.delete(item)

            # Insert transactions
            for transaction in transactions:

                self.table.insert(
                    "",
                    tk.END,
                    values=(
                        transaction["transaction_id"],
                        transaction["product_name"],
                        transaction["transaction_type"],
                        transaction["quantity"],
                        transaction["transaction_date"]
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Failed to load transactions.\n\n{e}"
            )


# Temporary testing
if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    ReportsWindow(root)

    root.mainloop()
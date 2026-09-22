import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


# Get all products
def get_products():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT product_id, product_name, quantity
        FROM products
        ORDER BY product_id
    """

    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


# Add stock
def stock_in(product_id, quantity):
    connection = get_connection()
    cursor = connection.cursor()

    # Increase product quantity
    query = """
        UPDATE products
        SET quantity = quantity + %s
        WHERE product_id = %s
    """

    cursor.execute(query, (quantity, product_id))

    # Record transaction
    query = """
        INSERT INTO stock_transactions
        (product_id, transaction_type, quantity)
        VALUES (%s, 'IN', %s)
    """

    cursor.execute(query, (product_id, quantity))

    connection.commit()

    cursor.close()
    connection.close()


# Remove stock
def stock_out(product_id, quantity):
    connection = get_connection()
    cursor = connection.cursor()

    # Check current stock
    query = """
        SELECT quantity
        FROM products
        WHERE product_id = %s
    """

    cursor.execute(query, (product_id,))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        connection.close()
        return False, "Product not found."

    current_quantity = result[0]

    # Prevent negative stock
    if quantity > current_quantity:
        cursor.close()
        connection.close()
        return False, "Not enough stock available."

    # Decrease product quantity
    query = """
        UPDATE products
        SET quantity = quantity - %s
        WHERE product_id = %s
    """

    cursor.execute(query, (quantity, product_id))

    # Record transaction
    query = """
        INSERT INTO stock_transactions
        (product_id, transaction_type, quantity)
        VALUES (%s, 'OUT', %s)
    """

    cursor.execute(query, (product_id, quantity))

    connection.commit()

    cursor.close()
    connection.close()

    return True, "Stock removed successfully."

class StockWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("StockFlow - Stock Management")
        self.window.geometry("750x500")
        self.window.resizable(False, False)

        self.create_widgets()
        self.load_products()

    def create_widgets(self):

        title = tk.Label(
            self.window,
            text="STOCK MANAGEMENT",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        # Product selection
        frame = tk.Frame(self.window)
        frame.pack(pady=10)

        tk.Label(
            frame,
            text="Product:",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=10, pady=10)

        self.product_combo = ttk.Combobox(
            frame,
            width=35,
            state="readonly"
        )
        self.product_combo.grid(row=0, column=1, padx=10)

        # Quantity
        tk.Label(
            frame,
            text="Quantity:",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=10, pady=10)

        self.quantity_entry = tk.Entry(
            frame,
            width=38
        )
        self.quantity_entry.grid(row=1, column=1, padx=10)

        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="STOCK IN",
            width=15,
            command=self.stock_in_action
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="STOCK OUT",
            width=15,
            command=self.stock_out_action
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            button_frame,
            text="CLEAR",
            width=15,
            command=self.clear
        ).grid(row=0, column=2, padx=10)

        # Product table
        columns = ("ID", "Product", "Quantity")

        self.table = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            height=12
        )

        self.table.heading("ID", text="ID")
        self.table.heading("Product", text="Product")
        self.table.heading("Quantity", text="Current Stock")

        self.table.column("ID", width=80)
        self.table.column("Product", width=350)
        self.table.column("Quantity", width=150)

        self.table.pack(pady=10)

    def load_products(self):

        products = get_products()

        # Update combo box
        self.product_combo["values"] = [
            f"{product['product_id']} - {product['product_name']}"
            for product in products
        ]

        # Clear table
        for item in self.table.get_children():
            self.table.delete(item)

        # Add products to table
        for product in products:
            self.table.insert(
                "",
                tk.END,
                values=(
                    product["product_id"],
                    product["product_name"],
                    product["quantity"]
                )
            )

    def stock_in_action(self):

        selected = self.product_combo.get()
        quantity = self.quantity_entry.get().strip()

        if not selected:
            messagebox.showwarning(
                "Missing Product",
                "Please select a product."
            )
            return

        if not quantity:
            messagebox.showwarning(
                "Missing Quantity",
                "Please enter a quantity."
            )
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number."
            )
            return

        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than 0."
            )
            return

        product_id = int(selected.split(" - ")[0])

        try:
            stock_in(product_id, quantity)

            messagebox.showinfo(
                "Success",
                "Stock added successfully!"
            )

            self.clear()
            self.load_products()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to add stock.\n\n{e}"
            )

    def stock_out_action(self):

        selected = self.product_combo.get()
        quantity = self.quantity_entry.get().strip()

        if not selected:
            messagebox.showwarning(
                "Missing Product",
                "Please select a product."
            )
            return

        if not quantity:
            messagebox.showwarning(
                "Missing Quantity",
                "Please enter a quantity."
            )
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number."
            )
            return

        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than 0."
            )
            return

        product_id = int(selected.split(" - ")[0])

        try:
            success, message = stock_out(product_id, quantity)

            if success:
                messagebox.showinfo(
                    "Success",
                    message
                )

                self.clear()
                self.load_products()

            else:
                messagebox.showwarning(
                    "Stock Error",
                    message
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to remove stock.\n\n{e}"
            )

    def clear(self):

        self.product_combo.set("")
        self.quantity_entry.delete(0, tk.END)


# Temporary testing
if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    StockWindow(root)

    root.mainloop()
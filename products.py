import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


# -----------------------------
# ADD PRODUCT
# -----------------------------

def add_product(name, category, price, quantity, reorder_level):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO products
        (product_name, category, price, quantity, reorder_level)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (name, category, price, quantity, reorder_level)
    )

    connection.commit()

    cursor.close()
    connection.close()


# -----------------------------
# GET ALL PRODUCTS
# -----------------------------

def get_products():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            product_id,
            product_name,
            category,
            price,
            quantity,
            reorder_level
        FROM products
        ORDER BY product_id
    """

    cursor.execute(query)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


# -----------------------------
# UPDATE PRODUCT
# -----------------------------

def update_product(
    product_id,
    name,
    category,
    price,
    quantity,
    reorder_level
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE products
        SET
            product_name = %s,
            category = %s,
            price = %s,
            quantity = %s,
            reorder_level = %s
        WHERE product_id = %s
    """

    cursor.execute(
        query,
        (
            name,
            category,
            price,
            quantity,
            reorder_level,
            product_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


# -----------------------------
# DELETE PRODUCT
# -----------------------------

def delete_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        DELETE FROM products
        WHERE product_id = %s
    """

    cursor.execute(
        query,
        (product_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()


# -----------------------------
# SEARCH PRODUCT
# -----------------------------

def search_product(name):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            product_id,
            product_name,
            category,
            price,
            quantity,
            reorder_level
        FROM products
        WHERE product_name LIKE %s
    """

    cursor.execute(
        query,
        (f"%{name}%",)
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

# -----------------------------
# PRODUCTS WINDOW
# -----------------------------

class ProductWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("StockFlow - Products")

        self.window.geometry("900x600")

        self.window.resizable(False, False)

        self.create_widgets()

        self.load_products()


    # -----------------------------
    # CREATE GUI
    # -----------------------------

    def create_widgets(self):

        title = tk.Label(
            self.window,
            text="PRODUCT MANAGEMENT",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=20)


        # FORM

        form_frame = tk.Frame(self.window)

        form_frame.pack()


        # Product Name

        tk.Label(
            form_frame,
            text="Product Name"
        ).grid(row=0, column=0, padx=10, pady=8)

        self.name_entry = tk.Entry(
            form_frame,
            width=30
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=8
        )


        # Category

        tk.Label(
            form_frame,
            text="Category"
        ).grid(row=1, column=0, padx=10, pady=8)

        self.category_entry = tk.Entry(
            form_frame,
            width=30
        )

        self.category_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )


        # Price

        tk.Label(
            form_frame,
            text="Price"
        ).grid(row=2, column=0, padx=10, pady=8)

        self.price_entry = tk.Entry(
            form_frame,
            width=30
        )

        self.price_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )


        # Quantity

        tk.Label(
            form_frame,
            text="Quantity"
        ).grid(row=3, column=0, padx=10, pady=8)

        self.quantity_entry = tk.Entry(
            form_frame,
            width=30
        )

        self.quantity_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=8
        )


        # Reorder Level

        tk.Label(
            form_frame,
            text="Reorder Level"
        ).grid(row=4, column=0, padx=10, pady=8)

        self.reorder_entry = tk.Entry(
            form_frame,
            width=30
        )

        self.reorder_entry.grid(
            row=4,
            column=1,
            padx=10,
            pady=8
        )


        # -----------------------------
        # BUTTONS
        # -----------------------------

        button_frame = tk.Frame(self.window)

        button_frame.pack(pady=10)


        tk.Button(
            button_frame,
            text="ADD",
            width=15,
            command=self.add
        ).grid(row=0, column=0, padx=5)


        tk.Button(
            button_frame,
            text="UPDATE",
            width=15,
            command=self.update
        ).grid(row=0, column=1, padx=5)


        tk.Button(
            button_frame,
            text="DELETE",
            width=15,
            command=self.delete
        ).grid(row=0, column=2, padx=5)


        tk.Button(
            button_frame,
            text="CLEAR",
            width=15,
            command=self.clear
        ).grid(row=0, column=3, padx=5)


        # -----------------------------
        # SEARCH
        # -----------------------------

        search_frame = tk.Frame(self.window)

        search_frame.pack(pady=5)


        tk.Label(
            search_frame,
            text="Search"
        ).pack(side="left", padx=5)


        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )


        tk.Button(
            search_frame,
            text="SEARCH",
            command=self.search
        ).pack(side="left", padx=5)


        tk.Button(
            search_frame,
            text="SHOW ALL",
            command=self.load_products
        ).pack(side="left", padx=5)


        # -----------------------------
        # TABLE
        # -----------------------------

        table_frame = tk.Frame(self.window)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )


        columns = (
            "ID",
            "Product",
            "Category",
            "Price",
            "Quantity",
            "Reorder"
        )


        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )


        for column in columns:

            self.table.heading(
                column,
                text=column
            )


        self.table.column(
            "ID",
            width=60
        )

        self.table.column(
            "Product",
            width=180
        )

        self.table.column(
            "Category",
            width=150
        )

        self.table.column(
            "Price",
            width=120
        )

        self.table.column(
            "Quantity",
            width=100
        )

        self.table.column(
            "Reorder",
            width=100
        )


        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )


        self.table.configure(
            yscrollcommand=scrollbar.set
        )


        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        # Select product

        self.table.bind(
            "<ButtonRelease-1>",
            self.select_product
        )

    # -----------------------------
    # LOAD PRODUCTS
    # -----------------------------

    def load_products(self):

        for item in self.table.get_children():

            self.table.delete(item)


        products = get_products()


        for product in products:

            self.table.insert(
                "",
                tk.END,
                values=(
                    product["product_id"],
                    product["product_name"],
                    product["category"],
                    f"{product['price']:.2f}",
                    product["quantity"],
                    product["reorder_level"]
                )
            )

        # -----------------------------
    # ADD PRODUCT
    # -----------------------------

    def add(self):

        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        reorder_level = self.reorder_entry.get().strip()

        # Check empty fields
        if not name or not category or not price or not quantity or not reorder_level:

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        # Convert values
        try:

            price = float(price)
            quantity = int(quantity)
            reorder_level = int(reorder_level)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Price must be a number.\n"
                "Quantity and Reorder Level must be whole numbers."
            )

            return

        # Check negative values
        if price < 0 or quantity < 0 or reorder_level < 0:

            messagebox.showerror(
                "Invalid Input",
                "Values cannot be negative."
            )

            return

        # Add to database
        try:

            add_product(
                name,
                category,
                price,
                quantity,
                reorder_level
            )

            messagebox.showinfo(
                "Success",
                "Product added successfully!"
            )

            self.clear_form()

            self.load_products()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Failed to add product.\n\n{e}"
            )

        # -----------------------------
    # CLEAR FORM
    # -----------------------------

    def clear_form(self):

        self.name_entry.delete(0, tk.END)

        self.category_entry.delete(0, tk.END)

        self.price_entry.delete(0, tk.END)

        self.quantity_entry.delete(0, tk.END)

        self.reorder_entry.delete(0, tk.END)

        self.search_entry.delete(0, tk.END)

        for item in self.table.selection():

            self.table.selection_remove(item)

        # -----------------------------
    # CLEAR BUTTON
    # -----------------------------

    def clear(self):

        self.clear_form()


    # -----------------------------
    # SELECT PRODUCT
    # -----------------------------

    def select_product(self, event):

        selected_item = self.table.focus()

        if not selected_item:
            return

        values = self.table.item(
            selected_item,
            "values"
        )

        if not values:
            return

        # Product Name
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        # Category
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, values[2])

        # Price
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, values[3])

        # Quantity
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, values[4])

        # Reorder Level
        self.reorder_entry.delete(0, tk.END)
        self.reorder_entry.insert(0, values[5])

        # -----------------------------
    # UPDATE PRODUCT
    # -----------------------------

    def update(self):

        selected_item = self.table.focus()

        if not selected_item:

            messagebox.showwarning(
                "No Selection",
                "Please select a product to update."
            )

            return

        values = self.table.item(
            selected_item,
            "values"
        )

        if not values:
            return

        product_id = values[0]

        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        reorder_level = self.reorder_entry.get().strip()

        # Check empty fields
        if not name or not category or not price or not quantity or not reorder_level:

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        # Convert values
        try:

            price = float(price)
            quantity = int(quantity)
            reorder_level = int(reorder_level)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Price must be a number.\n"
                "Quantity and Reorder Level must be whole numbers."
            )

            return

        # Check negative values
        if price < 0 or quantity < 0 or reorder_level < 0:

            messagebox.showerror(
                "Invalid Input",
                "Values cannot be negative."
            )

            return

        # Confirmation
        result = messagebox.askyesno(
            "Confirm Update",
            "Are you sure you want to update this product?"
        )

        if not result:
            return

        # Update database
        try:

            update_product(
                product_id,
                name,
                category,
                price,
                quantity,
                reorder_level
            )

            messagebox.showinfo(
                "Success",
                "Product updated successfully!"
            )

            self.clear_form()

            self.load_products()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Failed to update product.\n\n{e}"
            )

        # -----------------------------
    # DELETE PRODUCT
    # -----------------------------

    def delete(self):

        selected_item = self.table.focus()

        if not selected_item:

            messagebox.showwarning(
                "No Selection",
                "Please select a product to delete."
            )

            return

        values = self.table.item(
            selected_item,
            "values"
        )

        if not values:
            return

        product_id = values[0]
        product_name = values[1]

        # Confirmation
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{product_name}'?"
        )

        if not result:
            return

        # Delete from database
        try:

            delete_product(product_id)

            messagebox.showinfo(
                "Success",
                "Product deleted successfully!"
            )

            self.clear_form()

            self.load_products()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Failed to delete product.\n\n{e}"
            )

        # -----------------------------
    # SEARCH PRODUCT
    # -----------------------------

    def search(self):

        name = self.search_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Search",
                "Please enter a product name."
            )

            return

        products = search_product(name)

        # Clear table

        for item in self.table.get_children():

            self.table.delete(item)

        # Display search results

        for product in products:

            self.table.insert(
                "",
                tk.END,
                values=(
                    product["product_id"],
                    product["product_name"],
                    product["category"],
                    f"{product['price']:.2f}",
                    product["quantity"],
                    product["reorder_level"]
                )
            )

        if not products:

            messagebox.showinfo(
                "Search",
                "No product found."
            )

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    ProductWindow(root)

    root.mainloop()
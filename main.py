import tkinter as tk
from tkinter import messagebox
import bcrypt

from database import get_connection


# Check username and password from MySQL
def check_login(username, password):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT user_id, username, password_hash, role
        FROM users
        WHERE username = %s
    """

    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        stored_password = user["password_hash"].encode("utf-8")

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        ):
            return user

    return None


# Login Window
class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("StockFlow - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="STOCKFLOW",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=30)

        tk.Label(
            self.root,
            text="Username"
        ).pack()

        self.username_entry = tk.Entry(
            self.root,
            width=30
        )
        self.username_entry.pack(pady=5)

        tk.Label(
            self.root,
            text="Password"
        ).pack()

        self.password_entry = tk.Entry(
            self.root,
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="LOGIN",
            width=15,
            command=self.login
        ).pack(pady=20)

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Check empty fields
        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )

            return

        try:

            # Check login from database
            user = check_login(username, password)

            if user:

                # Close login window
                self.root.destroy()

                # Open dashboard
                dashboard = tk.Tk()

                DashboardWindow(dashboard)

                dashboard.mainloop()

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to login.\n\n{e}"
            )


# Dashboard Window
class DashboardWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("StockFlow - Dashboard")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="STOCKFLOW DASHBOARD",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=30)

        # Products button
        tk.Button(
            self.root,
            text="PRODUCTS",
            width=25,
            height=2,
            command=self.open_products
        ).pack(pady=10)

        # Stock button
        tk.Button(
            self.root,
            text="STOCK",
            width=25,
            height=2,
            command=self.open_stock
        ).pack(pady=10)

        # Reports button
        tk.Button(
            self.root,
            text="REPORTS",
            width=25,
            height=2,
            command=self.open_reports
        ).pack(pady=10)

        # Exit button
        tk.Button(
            self.root,
            text="EXIT",
            width=25,
            height=2,
            command=self.root.destroy
        ).pack(pady=20)

    def open_products(self):

        from products import ProductWindow

        ProductWindow(self.root)

    def open_stock(self):

        from stock import StockWindow

        StockWindow(self.root)

    def open_reports(self):

        from reports import ReportsWindow

        ReportsWindow(self.root)


# Start application
if __name__ == "__main__":

    root = tk.Tk()

    LoginWindow(root)

    root.mainloop()
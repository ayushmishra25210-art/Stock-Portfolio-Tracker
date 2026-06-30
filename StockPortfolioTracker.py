import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import random


STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 330,
    "AMZN": 145,
    "NVDA": 900,
    "META": 480,
    "NFLX": 600
}


CUSTOMERS = {
    "CUST1001": {
        "name": "Admin User",
        "password": "1234"
    }
}


class StockPortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("1050x720")
        self.root.resizable(False, False)

        self.current_customer_id = ""
        self.current_customer_name = ""
        self.portfolio = []

        self.setup_style()
        self.show_login_page()

    def setup_style(self):
        self.root.configure(bg="white")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#111827",
            rowheight=35,
            fieldbackground="white",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#b91c1c",
            foreground="white",
            font=("Arial", 11, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#ef4444")]
        )

        style.configure(
            "TCombobox",
            font=("Arial", 12)
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_login_page(self):
        self.clear_window()

        main = tk.Frame(self.root, bg="white")
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg="#b91c1c", width=420)
        left.pack(side="left", fill="y")

        tk.Label(
            left,
            text="StockPro",
            bg="#b91c1c",
            fg="white",
            font=("Arial", 36, "bold")
        ).pack(pady=(170, 10))

        tk.Label(
            left,
            text="Real-Time Style\nStock Portfolio Tracker",
            bg="#b91c1c",
            fg="#fee2e2",
            font=("Arial", 18, "bold"),
            justify="center"
        ).pack(pady=10)

        tk.Label(
            left,
            text="Track your investment value\nusing manually defined stock prices.",
            bg="#b91c1c",
            fg="white",
            font=("Arial", 12),
            justify="center"
        ).pack(pady=30)

        right = tk.Frame(main, bg="white")
        right.pack(side="right", fill="both", expand=True)

        card = tk.Frame(
            right,
            bg="white",
            highlightbackground="#fecaca",
            highlightthickness=2
        )
        card.place(x=145, y=110, width=390, height=480)

        tk.Label(
            card,
            text="Customer Login",
            bg="white",
            fg="#991b1b",
            font=("Arial", 24, "bold")
        ).pack(pady=(35, 8))

        tk.Label(
            card,
            text="Login to open your portfolio dashboard",
            bg="white",
            fg="#6b7280",
            font=("Arial", 10)
        ).pack(pady=(0, 25))

        tk.Label(
            card,
            text="Customer ID",
            bg="white",
            fg="#374151",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=40)

        self.login_id_entry = tk.Entry(card, font=("Arial", 13), bd=1, relief="solid")
        self.login_id_entry.pack(padx=40, pady=8, fill="x", ipady=7)

        tk.Label(
            card,
            text="Password",
            bg="white",
            fg="#374151",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=40, pady=(10, 0))

        self.login_password_entry = tk.Entry(card, font=("Arial", 13), bd=1, relief="solid", show="*")
        self.login_password_entry.pack(padx=40, pady=8, fill="x", ipady=7)

        tk.Button(
            card,
            text="Login",
            bg="#dc2626",
            fg="white",
            font=("Arial", 13, "bold"),
            bd=0,
            cursor="hand2",
            command=self.login_customer
        ).pack(padx=40, pady=(20, 10), fill="x", ipady=9)

        tk.Button(
            card,
            text="New Customer Registration",
            bg="white",
            fg="#dc2626",
            font=("Arial", 11, "bold"),
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.show_register_page
        ).pack(padx=40, pady=5, fill="x", ipady=8)

        tk.Button(
            card,
            text="Forgot Password?",
            bg="white",
            fg="#991b1b",
            font=("Arial", 10, "bold"),
            bd=0,
            cursor="hand2",
            command=self.show_forgot_password_page
        ).pack(pady=10)

        tk.Label(
            card,
            text="Demo Login: CUST1001 / 1234",
            bg="white",
            fg="#6b7280",
            font=("Arial", 9)
        ).pack(pady=5)

    def login_customer(self):
        customer_id = self.login_id_entry.get().strip()
        password = self.login_password_entry.get().strip()

        if customer_id == "" or password == "":
            messagebox.showerror("Login Error", "Please enter Customer ID and Password.")
            return

        if customer_id in CUSTOMERS and CUSTOMERS[customer_id]["password"] == password:
            self.current_customer_id = customer_id
            self.current_customer_name = CUSTOMERS[customer_id]["name"]
            messagebox.showinfo("Login Successful", f"Welcome {self.current_customer_name}")
            self.show_main_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Customer ID or Password.")

    def show_register_page(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="New Customer Registration",
            bg="white",
            fg="#991b1b",
            font=("Arial", 26, "bold")
        ).pack(pady=(70, 10))

        tk.Label(
            frame,
            text="Create your new customer account",
            bg="white",
            fg="#6b7280",
            font=("Arial", 11)
        ).pack(pady=(0, 25))

        card = tk.Frame(
            frame,
            bg="white",
            highlightbackground="#fecaca",
            highlightthickness=2
        )
        card.pack()
        card.config(width=430, height=390)
        card.pack_propagate(False)

        tk.Label(card, text="Full Name", bg="white", fg="#374151", font=("Arial", 11, "bold")).pack(anchor="w", padx=45, pady=(35, 0))
        self.reg_name_entry = tk.Entry(card, font=("Arial", 13), bd=1, relief="solid")
        self.reg_name_entry.pack(padx=45, pady=8, fill="x", ipady=7)

        tk.Label(card, text="Create Password", bg="white", fg="#374151", font=("Arial", 11, "bold")).pack(anchor="w", padx=45, pady=(10, 0))
        self.reg_password_entry = tk.Entry(card, font=("Arial", 13), bd=1, relief="solid", show="*")
        self.reg_password_entry.pack(padx=45, pady=8, fill="x", ipady=7)

        tk.Label(card, text="Confirm Password", bg="white", fg="#374151", font=("Arial", 11, "bold")).pack(anchor="w", padx=45, pady=(10, 0))
        self.reg_confirm_entry = tk.Entry(card, font=("Arial", 13), bd=1, relief="solid", show="*")
        self.reg_confirm_entry.pack(padx=45, pady=8, fill="x", ipady=7)

        tk.Button(
            card,
            text="Create Customer ID",
            bg="#dc2626",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            cursor="hand2",
            command=self.register_customer
        ).pack(padx=45, pady=(22, 8), fill="x", ipady=8)

        tk.Button(
            card,
            text="Back to Login",
            bg="white",
            fg="#dc2626",
            font=("Arial", 11, "bold"),
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.show_login_page
        ).pack(padx=45, pady=5, fill="x", ipady=7)

    def register_customer(self):
        name = self.reg_name_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        confirm = self.reg_confirm_entry.get().strip()

        if name == "" or password == "" or confirm == "":
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        customer_id = "CUST" + str(random.randint(1000, 9999))

        while customer_id in CUSTOMERS:
            customer_id = "CUST" + str(random.randint(1000, 9999))

        CUSTOMERS[customer_id] = {
            "name": name,
            "password": password
        }

        messagebox.showinfo(
            "Registration Successful",
            f"Account created successfully!\n\nYour Customer ID is: {customer_id}\n\nUse this ID for login."
        )

        self.show_login_page()

    def show_forgot_password_page(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Forgot Password",
            bg="white",
            fg="#991b1b",
            font=("Arial", 26, "bold")
        ).pack(pady=(90, 10))

        tk.Label(
            frame,
            text="Reset password using Customer ID",
            bg="white",
            fg="#6b7280",
            font=("Arial", 11)
        ).pack(pady=(0, 25))

        card = tk.Frame(
            frame,
            bg="white",
            highlightbackground="#fecaca",
            highlightthickness=2
        )
        card.pack()
        card.config(width=430, height=330)
        card.pack_propagate(False)

        tk.Label(card, text="Customer ID", bg="white", fg="#374151", font=("Arial", 11, "bold")).pack(anchor="w", padx=45, pady=(35, 0))
        self.forgot_id_entry = tk.Entry(card, font=("Arial", 13), bd=1, relief="solid")
        self.forgot_id_entry.pack(padx=45, pady=8, fill="x", ipady=7)

        tk.Label(card, text="New Password", bg="white", fg="#374151", font=("Arial", 11, "bold")).pack(anchor="w", padx=45, pady=(10, 0))
        self.forgot_password_entry = tk.Entry(card, font=("Arial", 13), bd=1, relief="solid", show="*")
        self.forgot_password_entry.pack(padx=45, pady=8, fill="x", ipady=7)

        tk.Button(
            card,
            text="Reset Password",
            bg="#dc2626",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            cursor="hand2",
            command=self.reset_password
        ).pack(padx=45, pady=(20, 8), fill="x", ipady=8)

        tk.Button(
            card,
            text="Back to Login",
            bg="white",
            fg="#dc2626",
            font=("Arial", 11, "bold"),
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.show_login_page
        ).pack(padx=45, pady=5, fill="x", ipady=7)

    def reset_password(self):
        customer_id = self.forgot_id_entry.get().strip()
        new_password = self.forgot_password_entry.get().strip()

        if customer_id == "" or new_password == "":
            messagebox.showerror("Error", "Please enter Customer ID and new password.")
            return

        if customer_id not in CUSTOMERS:
            messagebox.showerror("Error", "Customer ID not found.")
            return

        CUSTOMERS[customer_id]["password"] = new_password
        messagebox.showinfo("Success", "Password reset successfully.")
        self.show_login_page()

    def show_main_dashboard(self):
        self.clear_window()

        header = tk.Frame(self.root, bg="#b91c1c", height=88)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Stock Portfolio Dashboard",
            bg="#b91c1c",
            fg="white",
            font=("Arial", 25, "bold")
        ).place(x=20, y=12)

        tk.Label(
            header,
            text=f"Customer: {self.current_customer_name}   |   ID: {self.current_customer_id}",
            bg="#b91c1c",
            fg="#fee2e2",
            font=("Arial", 11, "bold")
        ).place(x=24, y=55)

        self.time_label = tk.Label(
            header,
            text="",
            bg="#b91c1c",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.time_label.place(x=755, y=22)

        tk.Label(
            header,
            text="â MARKET WATCH ACTIVE",
            bg="#b91c1c",
            fg="white",
            font=("Arial", 11, "bold")
        ).place(x=755, y=52)

        self.update_clock()

        nav = tk.Frame(
            self.root,
            bg="white",
            height=65,
            highlightbackground="#fecaca",
            highlightthickness=1
        )
        nav.pack(fill="x")

        tk.Button(
            nav,
            text="Portfolio",
            bg="#dc2626",
            fg="white",
            activebackground="#991b1b",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            bd=0,
            cursor="hand2",
            command=self.show_portfolio_page
        ).pack(side="left", padx=20, pady=12, ipadx=30, ipady=8)

        tk.Button(
            nav,
            text="Add Stock",
            bg="white",
            fg="#991b1b",
            activebackground="#fee2e2",
            activeforeground="#991b1b",
            font=("Arial", 11, "bold"),
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.show_add_stock_page
        ).pack(side="left", padx=10, pady=12, ipadx=30, ipady=8)

        tk.Button(
            nav,
            text="Logout",
            bg="white",
            fg="#dc2626",
            activebackground="#fee2e2",
            activeforeground="#991b1b",
            font=("Arial", 11, "bold"),
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.logout
        ).pack(side="right", padx=30, pady=12, ipadx=30, ipady=8)

        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill="both", expand=True)

        self.show_add_stock_page()

    def update_clock(self):
        if hasattr(self, "time_label"):
            current_time = datetime.now().strftime("%d-%m-%Y  |  %I:%M:%S %p")
            self.time_label.config(text=current_time)
            self.root.after(1000, self.update_clock)

    def show_add_stock_page(self):
        self.clear_content()

        title = tk.Label(
            self.content_frame,
            text="Add Stock Holding",
            bg="white",
            fg="#991b1b",
            font=("Arial", 25, "bold")
        )
        title.pack(pady=(30, 5))

        subtitle = tk.Label(
            self.content_frame,
            text="Select stock symbol and enter quantity to calculate investment",
            bg="white",
            fg="#6b7280",
            font=("Arial", 11)
        )
        subtitle.pack(pady=(0, 20))

        card = tk.Frame(
            self.content_frame,
            bg="white",
            highlightbackground="#fecaca",
            highlightthickness=2
        )
        card.pack()
        card.config(width=450, height=390)
        card.pack_propagate(False)

        tk.Label(
            card,
            text="Stock Symbol",
            bg="white",
            fg="#374151",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=55, pady=(35, 0))

        self.stock_var = tk.StringVar()

        self.stock_combo = ttk.Combobox(
            card,
            textvariable=self.stock_var,
            values=list(STOCK_PRICES.keys()),
            font=("Arial", 13),
            state="readonly"
        )
        self.stock_combo.pack(padx=55, pady=8, fill="x", ipady=4)
        self.stock_combo.set("AAPL")
        self.stock_combo.bind("<<ComboboxSelected>>", self.update_price_label)

        tk.Label(
            card,
            text="Quantity",
            bg="white",
            fg="#374151",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=55, pady=(15, 0))

        self.quantity_entry = tk.Entry(
            card,
            font=("Arial", 13),
            bd=1,
            relief="solid"
        )
        self.quantity_entry.pack(padx=55, pady=8, fill="x", ipady=8)

        price_box = tk.Frame(card, bg="#fee2e2")
        price_box.pack(padx=55, pady=18, fill="x")

        tk.Label(
            price_box,
            text="Current Manual Price",
            bg="#fee2e2",
            fg="#7f1d1d",
            font=("Arial", 10, "bold")
        ).pack(pady=(10, 0))

        self.price_label = tk.Label(
            price_box,
            text="â¹180",
            bg="#fee2e2",
            fg="#b91c1c",
            font=("Arial", 24, "bold")
        )
        self.price_label.pack(pady=(0, 10))

        tk.Button(
            card,
            text="Add to Portfolio",
            bg="#dc2626",
            fg="white",
            activebackground="#991b1b",
            activeforeground="white",
            font=("Arial", 12, "bold"),
            bd=0,
            cursor="hand2",
            command=self.add_stock
        ).pack(padx=55, pady=8, fill="x", ipady=9)

        tk.Button(
            card,
            text="View Portfolio",
            bg="white",
            fg="#dc2626",
            activebackground="#fee2e2",
            activeforeground="#991b1b",
            font=("Arial", 11, "bold"),
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.show_portfolio_page
        ).pack(padx=55, pady=5, fill="x", ipady=7)

    def update_price_label(self, event=None):
        stock = self.stock_var.get()
        price = STOCK_PRICES.get(stock, 0)
        self.price_label.config(text=f"â¹{price}")

    def add_stock(self):
        stock = self.stock_var.get()
        quantity = self.quantity_entry.get().strip()

        if stock == "":
            messagebox.showerror("Input Error", "Please select a stock symbol.")
            return

        if quantity == "":
            messagebox.showerror("Input Error", "Please enter quantity.")
            return

        try:
            quantity = int(quantity)

            if quantity <= 0:
                messagebox.showerror("Input Error", "Quantity must be greater than 0.")
                return

        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a valid number.")
            return

        price = STOCK_PRICES[stock]
        investment = quantity * price

        self.portfolio.append({
            "stock": stock,
            "quantity": quantity,
            "price": price,
            "investment": investment,
            "status": "Tracked"
        })

        messagebox.showinfo(
            "Stock Added",
            f"{stock} added successfully!\n\nQuantity: {quantity}\nPrice: â¹{price}\nInvestment: â¹{investment}"
        )

        self.show_portfolio_page()

    def show_portfolio_page(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="Portfolio Overview",
            bg="white",
            fg="#991b1b",
            font=("Arial", 25, "bold")
        ).pack(pady=(25, 5))

        tk.Label(
            self.content_frame,
            text="Your added stocks and total investment value",
            bg="white",
            fg="#6b7280",
            font=("Arial", 11)
        ).pack(pady=(0, 15))

        table_frame = tk.Frame(
            self.content_frame,
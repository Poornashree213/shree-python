import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def connect_db():
    try:
        # Connecting to your MySQL database
        return mysql.connector.connect(host="localhost", user="root", password="root", database="icecreamshopdb")  # Changed database name
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def fetch_ice_creams():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT flavor, size, price FROM icecreams")  # Changed table name from `bikes` to `icecreams`
        ice_creams = cursor.fetchall()
        conn.close()
        return ice_creams
    return []

def add_ice_cream():
    flavor = flavor_entry.get()
    size = size_entry.get()
    price = price_entry.get()
    if flavor.lower() == "exit":
        root.quit()
    elif flavor and size and price:
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid price.")
            return
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO icecreams (flavor, size, price) VALUES (%s, %s, %s)", (flavor, size, price))  # Changed table and column names
            conn.commit()
            conn.close()
        ice_cream_table.insert("", tk.END, values=(flavor, size, f"${price:.2f}"))
        flavor_entry.delete(0, tk.END)
        size_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

def add_to_cart():
    selected = ice_cream_table.selection()
    for item in selected:
        cart_table.insert("", tk.END, values=ice_cream_table.item(item, "values"))
    calculate_total()

def remove_from_cart():
    for item in cart_table.selection():
        cart_table.delete(item)
    calculate_total()

def calculate_total():
    total = sum(float(cart_table.item(item, "values")[2][1:]) for item in cart_table.get_children())
    total_label.config(text=f"Total: ${total:.2f}")

def checkout():
    if cart_table.get_children():
        messagebox.showinfo("Success", "Purchase Successful!")
        cart_table.delete(*cart_table.get_children())
        total_label.config(text="Total: $0.00")

root = tk.Tk()
root.configure(bg="#fff0f0")  # Background color changed to a light pink for an ice cream theme
root.title("Ibaco Ice Cream Shop")
root.geometry("600x500")

# Title Label with customized font
title_label = tk.Label(root, text="Welcome to Ibaco Ice Cream Shop", font=("Helvetica", 20, "bold"), fg="#FF4081", bg="#fff0f0")
title_label.pack(pady=20)

# Ice Cream List Label
ice_cream_label = tk.Label(root, text="Ice Creams Available", font=("Arial", 16), fg="black", bg="#fff0f0")
ice_cream_label.pack()

# Ice Cream Table with customized style
ice_cream_table = ttk.Treeview(root, columns=("Flavor", "Size", "Price"), show="headings", height=5)
ice_cream_table.heading("Flavor", text="Flavor")
ice_cream_table.heading("Size", text="Size")
ice_cream_table.heading("Price", text="Price")
ice_cream_table.column("Flavor", anchor="center")
ice_cream_table.column("Size", anchor="center")
ice_cream_table.column("Price", anchor="center")
ice_cream_table.pack(pady=10)

# Sample Ice Creams Data
sample_ice_creams = [
    ("Vanilla", "Small", 3.50),
    ("Chocolate", "Medium", 4.00),
    ("Strawberry", "Large", 5.00),
    ("Mango", "Small", 3.80),
    ("Pistachio", "Large", 6.00)
]

for ice_cream in sample_ice_creams:
    ice_cream_table.insert("", tk.END, values=(ice_cream[0], ice_cream[1], f"${ice_cream[2]:.2f}"))

# Add to Cart Button with customized style
add_cart_button = tk.Button(root, text="Add to Cart", command=add_to_cart, bg="#FF4081", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3)
add_cart_button.pack(pady=10)

# New Ice Cream Form Section
new_ice_cream_label = tk.Label(root, text="Add a New Ice Cream", font=("Arial", 14, "bold"), fg="black", bg="#fff0f0")
new_ice_cream_label.pack(pady=10)

# New Ice Cream Fields
flavor_entry = tk.Entry(root, font=("Arial", 12), bd=2, relief="solid", width=25)
flavor_entry.pack(pady=5)

size_entry = tk.Entry(root, font=("Arial", 12), bd=2, relief="solid", width=25)
size_entry.pack(pady=5)

price_entry = tk.Entry(root, font=("Arial", 12), bd=2, relief="solid", width=25)
price_entry.pack(pady=5)

# Add Ice Cream Button with customized style
add_ice_cream_button = tk.Button(root, text="Add Ice Cream", command=add_ice_cream, bg="#FF9800", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3)
add_ice_cream_button.pack(pady=10)

# Cart Section
cart_label = tk.Label(root, text="Cart", font=("Arial", 16), fg="black", bg="#fff0f0")
cart_label.pack(pady=10)

cart_table = ttk.Treeview(root, columns=("Flavor", "Size", "Price"), show="headings", height=5)
cart_table.heading("Flavor", text="Flavor")
cart_table.heading("Size", text="Size")
cart_table.heading("Price", text="Price")
cart_table.column("Flavor", anchor="center")
cart_table.column("Size", anchor="center")
cart_table.column("Price", anchor="center")
cart_table.pack(pady=10)

# Remove Ice Cream from Cart Button
remove_cart_button = tk.Button(root, text="Remove from Cart", command=remove_from_cart, bg="#F44336", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3)
remove_cart_button.pack(pady=10)

# Total Price Label
total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 14), fg="#4CAF50", bg="#fff0f0")
total_label.pack(pady=10)

# Checkout Button
checkout_button = tk.Button(root, text="Checkout", command=checkout, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3)
checkout_button.pack(pady=20)

root.mainloop()

	


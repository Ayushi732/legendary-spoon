import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# --- Connect to MySQL ---
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ayushi12@3",   # change if needed
        database="food_ordering"
    )
    cursor = db.cursor()
except Exception as e:
    messagebox.showerror("Database Error", f"Cannot connect to MySQL:\n{e}")
    exit()

# --- Create required tables if not exist ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(50),
    price INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(50),
    total INT
)
""")
db.commit()

# --- Main Window ---
root = tk.Tk()
root.title("🍔 Food Ordering System")
root.geometry("720x650")
root.config(bg="#fffdf5")

# --- Title ---
tk.Label(root, text="🍕 FOOD ORDERING SYSTEM 🍔",
         font=("Comic Sans MS", 24, "bold"), bg="#fffdf5", fg="#e67e22").pack(pady=15)

# --- Customer Name Entry ---
name_frame = tk.Frame(root, bg="#fffdf5")
name_frame.pack(pady=5)
tk.Label(name_frame, text="Customer Name:", font=("Arial", 13), bg="#fffdf5").pack(side=tk.LEFT)
customer_entry = tk.Entry(name_frame, font=("Arial", 13))
customer_entry.pack(side=tk.LEFT, padx=10)

# --- Menu Frame ---
menu_frame = tk.Frame(root, bg="#fffdf5")
menu_frame.pack(pady=10)
tk.Label(menu_frame, text="📋 MENU", font=("Arial", 18, "bold"),
         bg="#fffdf5", fg="#e67e22").pack()

# Treeview (Menu List)
tree = ttk.Treeview(menu_frame, columns=("ID", "Item", "Price"), show="headings", height=6)
tree.heading("ID", text="ID")
tree.heading("Item", text="Item Name")
tree.heading("Price", text="Price (Rs)")
tree.column("ID", width=60, anchor="center")
tree.column("Item", width=280)
tree.column("Price", width=120, anchor="center")
tree.pack(pady=5)

# --- Load Menu from Database ---
def load_menu():
    tree.delete(*tree.get_children())  # clear old items
    cursor.execute("SELECT * FROM menu")
    rows = cursor.fetchall()
    if not rows:
        # Insert sample menu if empty
        sample_items = [
            ("Margherita Pizza", 200),
            ("Cheese Burger", 120),
            ("French Fries", 80),
            ("Cold Coffee", 90),
            ("Ice Cream", 70),
            ("White Sauce Pasta", 150)
        ]
        cursor.executemany("INSERT INTO menu (item_name, price) VALUES (%s, %s)", sample_items)
        db.commit()
        cursor.execute("SELECT * FROM menu")
        rows = cursor.fetchall()

    for item in rows:
        name = item[1]
        if "pizza" in name.lower():
            name = "🍕 " + name
        elif "burger" in name.lower():
            name = "🍔 " + name
        elif "pasta" in name.lower():
            name = "🍝 " + name
        elif "fries" in name.lower():
            name = "🍟 " + name
        elif "coffee" in name.lower():
            name = "☕ " + name
        elif "ice" in name.lower():
            name = "🍦 " + name
        tree.insert("", tk.END, values=(item[0], name, item[2]))

load_menu()

# --- Input Section for Order ---
order_frame = tk.Frame(root, bg="#fffdf5")
order_frame.pack(pady=10)

tk.Label(order_frame, text="Item ID:", font=("Arial", 12), bg="#fffdf5").grid(row=0, column=0, padx=5)
item_id_entry = tk.Entry(order_frame, width=10, font=("Arial", 12))
item_id_entry.grid(row=0, column=1, padx=5)

tk.Label(order_frame, text="Quantity:", font=("Arial", 12), bg="#fffdf5").grid(row=0, column=2, padx=5)
qty_entry = tk.Entry(order_frame, width=10, font=("Arial", 12))
qty_entry.grid(row=0, column=3, padx=5)

# --- Order Summary Section ---
tk.Label(root, text="🧾 ORDER SUMMARY", font=("Arial", 16, "bold"),
         bg="#fffdf5", fg="#e67e22").pack(pady=5)

order_list = tk.Listbox(root, width=70, height=10,
                        font=("Arial", 12), bg="#fff8e7", fg="#2c3e50")
order_list.pack(pady=5)

total_amount = tk.IntVar(value=0)
ordered_items = []

# --- Update Total Label ---
def update_total_label():
    total_label.config(
        text=f"💰 Total Bill: Rs.{total_amount.get()}",
        fg="#16a085"
    )

# --- Add Item Function ---
def add_item():
    try:
        item_id = item_id_entry.get().strip()
        qty_text = qty_entry.get().strip()

        if not item_id or not qty_text:
            messagebox.showwarning("Warning", "Please enter Item ID and Quantity.")
            return

        qty = int(qty_text)
        if qty <= 0:
            messagebox.showwarning("Warning", "Quantity must be greater than zero.")
            return

        cursor.execute("SELECT item_name, price FROM menu WHERE id=%s", (item_id,))
        item = cursor.fetchone()

        if item:
            name, price = item
            subtotal = price * qty
            ordered_items.append((name, qty, subtotal))
            order_list.insert(tk.END, f"{name} x{qty} = Rs.{subtotal}")
            total_amount.set(total_amount.get() + subtotal)
            update_total_label()
        else:
            messagebox.showerror("Error", "Invalid Item ID.")
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Place Order Function ---
def place_order():
    customer = customer_entry.get().strip()

    if not customer:
        messagebox.showwarning("Warning", "Please enter customer name.")
        return

    if not ordered_items:
        messagebox.showwarning("Warning", "No items added to the order.")
        return

    cursor.execute("INSERT INTO orders (customer_name, total) VALUES (%s, %s)",
                   (customer, total_amount.get()))
    db.commit()

    messagebox.showinfo("Success",
                        f"✅ Order placed for {customer}!\nTotal Bill: Rs.{total_amount.get()}")
    reset_order()

# --- Reset Order Function ---
def reset_order():
    ordered_items.clear()
    order_list.delete(0, tk.END)
    total_amount.set(0)
    update_total_label()
    item_id_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    customer_entry.delete(0, tk.END)

# --- Buttons ---
btn_frame = tk.Frame(root, bg="#fffdf5")
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="➕ Add Item", command=add_item,
                    bg="#e67e22", fg="white", font=("Arial", 13, "bold"), width=12)
add_btn.grid(row=0, column=0, padx=10)

place_btn = tk.Button(btn_frame, text="✅ Place Order", command=place_order,
                      bg="#16a085", fg="white", font=("Arial", 13, "bold"), width=14)
place_btn.grid(row=0, column=1, padx=10)

exit_btn = tk.Button(btn_frame, text="❌ Exit", command=root.destroy,
                     bg="#c0392b", fg="white", font=("Arial", 13, "bold"), width=10)
exit_btn.grid(row=0, column=2, padx=10)

# --- Total Label ---
total_label = tk.Label(root, text="💰 Total Bill: Rs.0",
                       font=("Arial", 15, "bold"), bg="#fffdf5", fg="#16a085")
total_label.pack(pady=10)

update_total_label()

root.mainloop()





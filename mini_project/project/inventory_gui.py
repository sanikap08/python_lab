import tkinter as tk
from tkinter import messagebox, ttk
import json


class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.inventory = {}
        self.minimum_stock_level = {}

        self.load_data()

        # GUI Layout
        self.create_widgets()

    def load_data(self, filename="inventory.json"):
        """Loads inventory data from a file."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.inventory = data.get("inventory", {})
                self.minimum_stock_level = data.get("minimum_stock_level", {})
        except FileNotFoundError:
            messagebox.showinfo("Info", "No existing inventory file found. Starting fresh.")

    def save_data(self, filename="inventory.json"):
        """Saves inventory data to a file."""
        data = {
            "inventory": self.inventory,
            "minimum_stock_level": self.minimum_stock_level,
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def create_widgets(self):
        """Creates the main GUI layout."""
        # Title
        title_label = tk.Label(self.root, text="Inventory Management System", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.create_add_item_tab()
        self.create_update_stock_tab()
        self.create_issue_material_tab()
        self.create_view_stock_tab()
        self.create_reorder_alert_tab()

    def create_add_item_tab(self):
        """Creates the Add Item tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Add Item")

        # Input fields
        tk.Label(tab, text="Item Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.item_name_entry = tk.Entry(tab)
        self.item_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(tab, text="Initial Quantity:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.initial_quantity_entry = tk.Entry(tab)
        self.initial_quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(tab, text="Minimum Stock Level:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.minimum_stock_entry = tk.Entry(tab)
        self.minimum_stock_entry.grid(row=2, column=1, padx=10, pady=10)

        # Add Button
        add_button = tk.Button(tab, text="Add Item", command=self.add_item)
        add_button.grid(row=3, column=0, columnspan=2, pady=20)

    def create_update_stock_tab(self):
        """Creates the Update Stock tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Update Stock")

        tk.Label(tab, text="Item Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.update_item_name_entry = tk.Entry(tab)
        self.update_item_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(tab, text="Quantity to Add/Remove:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.update_quantity_entry = tk.Entry(tab)
        self.update_quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        update_button = tk.Button(tab, text="Update Stock", command=self.update_stock)
        update_button.grid(row=2, column=0, columnspan=2, pady=20)

    def create_issue_material_tab(self):
        """Creates the Issue Material tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Issue Material")

        tk.Label(tab, text="Item Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.issue_item_name_entry = tk.Entry(tab)
        self.issue_item_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(tab, text="Quantity to Issue:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.issue_quantity_entry = tk.Entry(tab)
        self.issue_quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        issue_button = tk.Button(tab, text="Issue Material", command=self.issue_material)
        issue_button.grid(row=2, column=0, columnspan=2, pady=20)

    def create_view_stock_tab(self):
        """Creates the View Stock tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="View Stock")

        self.stock_text = tk.Text(tab, width=60, height=20, state="disabled")
        self.stock_text.pack(pady=10)

        view_button = tk.Button(tab, text="Refresh Stock", command=self.view_stock)
        view_button.pack()

    def create_reorder_alert_tab(self):
        """Creates the Reorder Alert tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reorder Alert")

        self.alert_text = tk.Text(tab, width=60, height=20, state="disabled")
        self.alert_text.pack(pady=10)

        alert_button = tk.Button(tab, text="Check Alerts", command=self.reorder_alert)
        alert_button.pack()

    def add_item(self):
        """Adds a new item to the inventory."""
        item_name = self.item_name_entry.get().strip()
        if item_name in self.inventory:
            messagebox.showerror("Error", "Item already exists in inventory.")
            return

        try:
            quantity = int(self.initial_quantity_entry.get())
            min_level = int(self.minimum_stock_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity and Minimum Stock Level must be integers.")
            return

        self.inventory[item_name] = quantity
        self.minimum_stock_level[item_name] = min_level
        messagebox.showinfo("Success", f"Item '{item_name}' added successfully!")
        self.save_data()

    def update_stock(self):
        """Updates stock for an item."""
        item_name = self.update_item_name_entry.get().strip()
        if item_name not in self.inventory:
            messagebox.showerror("Error", "Item not found in inventory.")
            return

        try:
            quantity = int(self.update_quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")
            return

        self.inventory[item_name] += quantity
        messagebox.showinfo("Success", f"Updated stock for '{item_name}'. New quantity: {self.inventory[item_name]}")
        self.save_data()

    def issue_material(self):
        """Issues material for production."""
        item_name = self.issue_item_name_entry.get().strip()
        if item_name not in self.inventory:
            messagebox.showerror("Error", "Item not found in inventory.")
            return

        try:
            quantity = int(self.issue_quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")
            return

        if self.inventory[item_name] < quantity:
            messagebox.showerror("Error", "Insufficient stock to issue.")
            return

        self.inventory[item_name] -= quantity
        messagebox.showinfo("Success", f"Issued {quantity} of '{item_name}'. Remaining stock: {self.inventory[item_name]}")
        self.save_data()

    def view_stock(self):
        """Displays current stock levels."""
        self.stock_text.config(state="normal")
        self.stock_text.delete("1.0", tk.END)
        for item, quantity in self.inventory.items():
            min_level = self.minimum_stock_level.get(item, "N/A")
            self.stock_text.insert(tk.END, f"{item}: {quantity} (Min Level: {min_level})\n")
        self.stock_text.config(state="disabled")

    def reorder_alert(self):
        """Checks for items below minimum stock levels."""
        self.alert_text.config(state="normal")
        self.alert_text.delete("1.0", tk.END)
        for item, quantity in self.inventory.items():
            if quantity < self.minimum_stock_level.get(item, 0):
                self.alert_text.insert(tk.END, f"Reorder Alert: {item} (Stock: {quantity})\n")
        self.alert_text.config(state="disabled")


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()

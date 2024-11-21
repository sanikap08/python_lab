import json

class InventoryManagementSystem:
    def __init__(self):
        self.inventory = {}
        self.minimum_stock_level = {}

    def load_data(self, filename="inventory.json"):
        """Loads inventory data from a file."""
        try:
            with open(filename, 'r') as file:
                data = file.read().strip()  # Read the file content
                if not data:  # If file is empty
                    print("Inventory file is empty. Starting fresh.")
                    return  # No need to load anything, just continue
                data = json.loads(data)  # Try parsing the data as JSON
                self.inventory = data.get("inventory", {})
                self.minimum_stock_level = data.get("minimum_stock_level", {})
        except FileNotFoundError:
            print("No existing inventory file found. Starting fresh.")
        except json.JSONDecodeError:
            print("Error decoding JSON from file. Starting fresh.")
            # Handle case where the file contains invalid JSON
        except Exception as e:
            print(f"Unexpected error: {e}")

    def save_data(self, filename="inventory.json"):
        """Saves inventory data to a file."""
        data = {
            "inventory": self.inventory,
            "minimum_stock_level": self.minimum_stock_level,
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def add_item(self):
        """Adds a new item to the inventory."""
        item_name = input("Enter item name: ").strip()
        if item_name in self.inventory:
            print("Item already exists in inventory.")
            return
        quantity = int(input("Enter initial quantity: "))
        min_level = int(input("Enter minimum stock level: "))
        self.inventory[item_name] = quantity
        self.minimum_stock_level[item_name] = min_level
        print(f"Item '{item_name}' added successfully!")

    def update_stock(self):
        """Updates the stock of an existing item."""
        item_name = input("Enter item name: ").strip()
        if item_name not in self.inventory:
            print("Item not found in inventory.")
            return
        quantity = int(input("Enter quantity to add/remove (use negative value to remove): "))
        self.inventory[item_name] += quantity
        print(f"Stock updated. Current quantity of '{item_name}': {self.inventory[item_name]}")

    def issue_material(self):
        """Issues material for production."""
        item_name = input("Enter item name to issue: ").strip()
        if item_name not in self.inventory:
            print("Item not found in inventory.")
            return
        quantity = int(input("Enter quantity to issue: "))
        if self.inventory[item_name] < quantity:
            print("Insufficient stock to issue.")
            return
        self.inventory[item_name] -= quantity
        print(f"Issued {quantity} of '{item_name}'. Remaining stock: {self.inventory[item_name]}")

    def check_stock(self):
        """Displays the current stock levels."""
        print("\nCurrent Stock Levels:")
        print("{:<20} {:<10} {:<10}".format("Item", "Quantity", "Min Level"))
        for item, quantity in self.inventory.items():
            min_level = self.minimum_stock_level.get(item, "N/A")
            print(f"{item:<20} {quantity:<10} {min_level:<10}")
        print()

    def reorder_alert(self):
        """Checks for items below minimum stock level and triggers alerts."""
        print("\nReorder Alert:")
        for item, quantity in self.inventory.items():
            if quantity < self.minimum_stock_level.get(item, 0):
                print(f"Item '{item}' is below minimum stock level. Current quantity: {quantity}")
        print()

    def run(self):
        """Runs the inventory management system."""
        self.load_data()
        while True:
            print("\nInventory Management System")
            print("1. Add New Item")
            print("2. Update Stock")
            print("3. Issue Material for Production")
            print("4. View Stock Levels")
            print("5. Reorder Alert")
            print("6. Exit")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.add_item()
            elif choice == "2":
                self.update_stock()
            elif choice == "3":
                self.issue_material()
            elif choice == "4":
                self.check_stock()
            elif choice == "5":
                self.reorder_alert()
            elif choice == "6":
                self.save_data()
                print("Exiting the system. Inventory data saved.")
                break
            else:
                print("Invalid choice! Please try again.")

# Main program
if __name__ == "__main__":
    system = InventoryManagementSystem()
    system.run()

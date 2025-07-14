import csv
import os
import datetime

INVENTORY_FILE = 'data/inventory.csv'
LOG_FILE = 'logs/inventory.log'


def log_transaction(message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")


def load_inventory():
    inventory = {}
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                item = row['Item Name']
                inventory[item] = {
                    'quantity': int(row['Quantity']),
                    'unit_price': float(row['Unit Price']),
                    'total_price': float(row['Total Price'])
                }
    return inventory


def save_inventory(inventory):
    os.makedirs(os.path.dirname(INVENTORY_FILE), exist_ok=True)
    with open(INVENTORY_FILE, mode='w', newline='') as file:
        fieldnames = ['Item Name', 'Quantity', 'Unit Price', 'Total Price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item, data in inventory.items():
            writer.writerow({
                'Item Name': item,
                'Quantity': data['quantity'],
                'Unit Price': f"{data['unit_price']:.2f}",
                'Total Price': f"{data['total_price']:.2f}"
            })


def add_stock(inventory):
    item = input("Enter item name: ").strip()
    try:
        qty = int(input("Enter quantity: "))
        price = float(input("Enter unit price: "))
    except ValueError:
        print("Invalid quantity or price.")
        return

    if item in inventory:
        inventory[item]['quantity'] += qty
        inventory[item]['total_price'] = inventory[item]['quantity'] * inventory[item]['unit_price']
    else:
        inventory[item] = {
            'quantity': qty,
            'unit_price': price,
            'total_price': qty * price
        }

    save_inventory(inventory)
    log_transaction(f"Added {qty} of '{item}' at ${price:.2f} each.")
    print("Stock added successfully.")


def remove_stock(inventory):
    item = input("Enter item name: ").strip()
    if item not in inventory:
        print("Item not found in inventory.")
        return

    try:
        qty = int(input("Enter quantity to remove: "))
    except ValueError:
        print("Invalid quantity.")
        return

    if qty <= 0:
        print("Quantity must be positive.")
        return

    if inventory[item]['quantity'] < qty:
        print("Not enough stock to remove.")
        return

    inventory[item]['quantity'] -= qty
    inventory[item]['total_price'] = inventory[item]['quantity'] * inventory[item]['unit_price']

    if inventory[item]['quantity'] == 0:
        del inventory[item]

    save_inventory(inventory)
    log_transaction(f"Removed {qty} of '{item}'.")
    print("Stock removed successfully.")


def view_inventory(inventory):
    if not inventory:
        print("Inventory is empty.")
        return

    print(f"{'Item Name':<20}{'Quantity':<10}{'Unit Price':<12}{'Total Price':<12}")
    print('-' * 54)
    total_value = 0
    for item, data in inventory.items():
        print(f"{item:<20}{data['quantity']:<10}{data['unit_price']:<12.2f}{data['total_price']:<12.2f}")
        total_value += data['total_price']

    print('-' * 54)
    print(f"{'Total Inventory Value:':<42}${total_value:.2f}")


def main():
    while True:
        print("\nInventory Menu")
        print("1. Add Incoming Stock")
        print("2. Remove/Outgoing Stock")
        print("3. View Inventory")
        print("4. Exit")

        choice = input("Choose an option: ").strip()
        inventory = load_inventory()

        if choice == '1':
            add_stock(inventory)
        elif choice == '2':
            remove_stock(inventory)
        elif choice == '3':
            view_inventory(inventory)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == '__main__':
    main()

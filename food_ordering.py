"""
**********MySQL code: **********

CREATE DATABASE IF NOT EXISTS food_ordering;

USE food_ordering;

CREATE TABLE IF NOT EXISTS menu (
    item_id   INT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    price     DECIMAL(10,2) NOT NULL
);


CREATE TABLE IF NOT EXISTS orders (
    order_id     INT AUTO_INCREMENT PRIMARY KEY,
    order_date   DATETIME NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL
);


CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id      INT NOT NULL,
    item_id       INT NOT NULL,
    quantity      INT NOT NULL,
    price         DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_order_items_menu
        FOREIGN KEY (item_id) REFERENCES menu(item_id)
);


INSERT IGNORE INTO menu (item_id, item_name, price) VALUES
    (1, 'Burger',   129.00),
    (2, 'Pizza',    199.00),
    (3, 'Sandwich', 99.00),
    (4, 'Juice',     49.00);

"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime

Database = {
    "host": "localhost",
    "user": "root",
    "password": "rosalynee",
    "database": "food_ordering"
}


def get_connection():
    try:
        connection = mysql.connector.connect(**Database)
        return connection
    except Error as e:
        print("Database connection failed:", e)
        return None


def view_menu(connection):
    menu_dict = {}
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT item_id, item_name, price FROM menu ORDER BY item_id")
        rows = cursor.fetchall()
        cursor.close()
        print("\n********** MENU **********")
        print(f"{'ID':<6}{'Item':<15}{'Price'}")
        print("\n")
        for item_id, item_name, price in rows:
            menu_dict[item_id] = {"name": item_name, "price": float(price)}
            print(f"{item_id:<6}{item_name:<15}Rs.{price}")
        print("\n")
    except Error as e:
        print("Error fetching menu:", e)
    return menu_dict


def place_order(menu_dict, current_order):
    if not menu_dict:
        print("Menu is empty. Cannot place an order right now.")
        return

    while True:
        item_input = input("Enter item ID: ").strip()
        if not item_input.isdigit():
            print("Invalid item ID. Please select an item from the menu.\n")
            continue

        item_id = int(item_input)
        if item_id not in menu_dict:
            print("Invalid item ID. Please select an item from the menu.\n")
            continue

        qty_input = input("Enter quantity: ").strip()
        if not qty_input.isdigit() or int(qty_input) < 1:
            print("Invalid quantity. Please enter a whole number of 1 or more.\n")
            continue

        quantity = int(qty_input)
        item_name = menu_dict[item_id]["name"]
        price = menu_dict[item_id]["price"]
        if item_id in current_order:
            current_order[item_id]["qty"] += quantity
        else:
            current_order[item_id] = {
                "name": item_name,
                "price": price,
                "qty": quantity
            }
        print(f"{item_name} x {quantity} added to order.\n")
        again = input("Do you want to add another item? (y/n): ").strip().lower()
        if again != "y":
            break


def view_current_order(current_order):
    if not current_order:
        print("\nYour order is empty.\n")
        return

    print("\n********** CURRENT ORDER **********")
    print(f"{'Item':<15}{'Quantity':<12}{'Price'}")
    print("\n")
    for data in current_order.values():
        print(f"{data['name']:<15}{data['qty']:<12}Rs.{data['price']}")
    print("******************************\n")


def generate_bill(current_order):
    if not current_order:
        print("\nCannot generate a bill: your order is empty.\n")
        return None
    print("\n")
    print("**********BILL**********")
    print("\n")
    grand_total = 0.0
    for data in current_order.values():
        item_total = data["price"] * data["qty"]
        grand_total += item_total
        print(f"{data['name']:<12} {data['qty']} x Rs.{data['price']} = Rs.{item_total:.2f}")
    print("\n******************************")
    print(f"Total{' ' * 20}Rs.{grand_total:.2f}")
    print("******************************\n")
    return grand_total


def confirm_order(connection, current_order, grand_total):
    if not current_order or grand_total is None:
        print("Cannot confirm an empty order.\n")
        return
    choice = input("Do you want to confirm the order? (y/n): ").strip().lower()
    if choice != "y":
        print("Order cancelled.\n")
        current_order.clear()
        return
    try:
        cursor = connection.cursor()
        order_date = datetime.now()
        cursor.execute(
            "INSERT INTO orders (order_date, total_amount) VALUES (%s, %s)",
            (order_date, grand_total)
        )
        order_id = cursor.lastrowid  

        for item_id, data in current_order.items():
            cursor.execute(
                """INSERT INTO order_items (order_id, item_id, quantity, price)
                   VALUES (%s, %s, %s, %s)""",
                (order_id, item_id, data["qty"], data["price"])
            )
        connection.commit()
        cursor.close()
        print("\nOrder confirmed successfully!")
        print(f"Order ID: {order_id}")
        print(f"Total Amount: Rs.{grand_total:.2f}\n")
        current_order.clear()

    except Error as e:
        connection.rollback()
        print("Error saving order to database:", e)


def view_previous_orders(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT order_id, order_date, total_amount FROM orders ORDER BY order_id")
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            print("\nNo previous orders found.\n")
            return
        print("\n********** PREVIOUS ORDERS **********")
        print(f"{'Order ID':<12}{'Date':<22}{'Total'}")
        print("\n")
        for order_id, order_date, total_amount in rows:
            print(f"{order_id:<12}{str(order_date):<22}Rs.{total_amount}")
        print("\n")
    except Error as e:
        print("Error fetching previous orders:", e)


def main():
    connection = get_connection()
    if connection is None:
        print("Could not connect to the database. Exiting.")
        return
    menu_dict = view_menu(connection)
    current_order = {}
    grand_total = None
    while True:
        print("******************************")
        print("       FOOD ORDERING SYSTEM")
        print("******************************")
        print("1. View Menu")
        print("2. Place Order")
        print("3. View Current Order")
        print("4. Generate Bill")
        print("5. Confirm Order")
        print("6. View Previous Orders")
        print("7. Exit")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            menu_dict = view_menu(connection)
        elif choice == "2":
            place_order(menu_dict, current_order)
        elif choice == "3":
            view_current_order(current_order)
        elif choice == "4":
            grand_total = generate_bill(current_order)
        elif choice == "5":
            confirm_order(connection, current_order, grand_total)
            grand_total = None 
        elif choice == "6":
            view_previous_orders(connection)
        elif choice == "7":
            print("Thank you for using the Food Ordering System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.\n")
    connection.close()


if __name__ == "__main__":
    main()

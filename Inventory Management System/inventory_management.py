"""
********** MySQL code **********

DROP DATABASE IF EXISTS inventory_management;
CREATE DATABASE inventory_management;
USE inventory_management;

CREATE TABLE Suppliers (
    supplier_id     INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name   VARCHAR(100) NOT NULL,
    phone           VARCHAR(20),
    email           VARCHAR(100),
    address         VARCHAR(255),
    CONSTRAINT chk_supplier_name CHECK (TRIM(supplier_name) <> '')
);

CREATE TABLE Products (
    product_id      INT AUTO_INCREMENT PRIMARY KEY,
    product_name    VARCHAR(100) NOT NULL,
    category        VARCHAR(50),
    supplier_id     INT,
    price           DECIMAL(10,2) NOT NULL,
    stock_quantity  INT NOT NULL DEFAULT 0,
    reorder_level   INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_product_supplier
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
        ON DELETE SET NULL,
    CONSTRAINT chk_product_name CHECK (TRIM(product_name) <> ''),
    CONSTRAINT chk_price_nonnegative CHECK (price >= 0),
    CONSTRAINT chk_stock_nonnegative CHECK (stock_quantity >= 0),
    CONSTRAINT chk_reorder_nonnegative CHECK (reorder_level >= 0)
);

CREATE TABLE Purchases (
    purchase_id     INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id     INT,
    purchase_date   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount    DECIMAL(10,2) NOT NULL DEFAULT 0,
    CONSTRAINT fk_purchase_supplier
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
        ON DELETE SET NULL,
    CONSTRAINT chk_purchase_total_nonnegative CHECK (total_amount >= 0)
);

CREATE TABLE Purchase_Items (
    purchase_item_id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id      INT NOT NULL,
    product_id       INT NOT NULL,
    quantity         INT NOT NULL,
    purchase_price   DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_pitem_purchase
        FOREIGN KEY (purchase_id) REFERENCES Purchases(purchase_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_pitem_product
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
    CONSTRAINT chk_pitem_qty_positive CHECK (quantity > 0),
    CONSTRAINT chk_pitem_price_nonnegative CHECK (purchase_price >= 0)
);

CREATE TABLE Sales (
    sale_id         INT AUTO_INCREMENT PRIMARY KEY,
    sale_date       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount    DECIMAL(10,2) NOT NULL DEFAULT 0,
    CONSTRAINT chk_sale_total_nonnegative CHECK (total_amount >= 0)
);

CREATE TABLE Sale_Items (
    sale_item_id    INT AUTO_INCREMENT PRIMARY KEY,
    sale_id         INT NOT NULL,
    product_id      INT NOT NULL,
    quantity        INT NOT NULL,
    selling_price   DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_sitem_sale
        FOREIGN KEY (sale_id) REFERENCES Sales(sale_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_sitem_product
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
    CONSTRAINT chk_sitem_qty_positive CHECK (quantity > 0),
    CONSTRAINT chk_sitem_price_nonnegative CHECK (selling_price >= 0)
);

INSERT INTO Suppliers (supplier_name, phone, email, address) VALUES
('ABC Distributors', '0000000000', 'abc@gmail.com', 'Kochi'),
('XYZ Suppliers', '1111111111', 'xyz@gmail.com', 'Kottayam'),
('Global Traders', '2222222222', 'global@gmail.com', 'Ernakulam');

INSERT INTO Products (product_name, category, supplier_id, price, stock_quantity, reorder_level) VALUES
('Keyboard', 'Electronics', 1, 800.00, 15, 5),
('Mouse', 'Electronics', 1, 400.00, 3, 5),
('Notebook', 'Stationery', 2, 80.00, 25, 10),
('USB Cable', 'Electronics', 3, 150.00, 2, 10),
('Pen', 'Stationery', 2, 10.00, 100, 20);

INSERT INTO Purchases (supplier_id, purchase_date, total_amount) VALUES
(1, '2026-09-09 11:20:00', 9000.00);

INSERT INTO Purchase_Items (purchase_id, product_id, quantity, purchase_price) VALUES
(1, 1, 10, 600.00),   
(1, 2, 10, 300.00);   

INSERT INTO Sales (sale_date, total_amount) VALUES
('2026-09-10 10:30:00', 960.00);

INSERT INTO Sale_Items (sale_id, product_id, quantity, selling_price) VALUES
(1, 1, 1, 800.00),
(1, 3, 2, 80.00);

"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "rosalynee",
    "database": "inventory_management"
}

def connect_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as err:
        print(f"\n[Database Connection Error] {err}")
        return None


def input_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def input_float(prompt, allow_negative=False):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if not allow_negative and value < 0:
                print("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def input_int(prompt, allow_negative=False):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if not allow_negative and value < 0:
                print("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number.")


def input_yes_no(prompt):
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please answer y or n.")


def add_product():
    print("\n********** ADD PRODUCT **********")
    name = input_nonempty("Product name: ")
    category = input("Category: ").strip()
    supplier_id = input_int("Supplier ID: ")
    price = input_float("Selling price: ")
    stock = input_int("Initial stock: ")
    reorder = input_int("Reorder level: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT supplier_id FROM Suppliers WHERE supplier_id = %s", (supplier_id,))
        if cursor.fetchone() is None:
            print(f"\nNo supplier found with ID {supplier_id}. Product not added.")
            return
        cursor.execute(
            """INSERT INTO Products (product_name, category, supplier_id, price, stock_quantity, reorder_level)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (name, category, supplier_id, price, stock, reorder)
        )
        conn.commit()
        print(f"\nProduct added successfully!\nProduct ID: {cursor.lastrowid}")
    except Error as err:
        print(f"\n[Database Error] {err}")
        conn.rollback()
    finally:
        conn.close()


def view_products():
    print("\n*************** PRODUCT LIST ***************")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.product_id, p.product_name, s.supplier_name,
                   p.category, p.price, p.stock_quantity, p.reorder_level
            FROM Products p
            LEFT JOIN Suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.product_id
        """)
        rows = cursor.fetchall()
        _print_product_table(rows)
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def _print_product_table(rows):
    if not rows:
        print("No products found.")
        return
    print(f"{'ID':<5}{'Product':<15}{'Supplier':<20}{'Category':<15}{'Price':<10}{'Stock':<8}{'Reorder':<8}")
    print("-" * 81)
    for pid, name, supplier, category, price, stock, reorder in rows:
        supplier = supplier or "N/A"
        print(f"{pid:<5}{name:<15}{supplier:<20}{category or '':<15}"
              f"Rs.{price:<7}{stock:<8}{reorder:<8}")


def search_products():
    print("\n********** SEARCH PRODUCTS **********")
    keyword = input_nonempty("Enter product name, category, or supplier keyword: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        like_pattern = f"%{keyword}%"
        cursor.execute("""
            SELECT p.product_id, p.product_name, s.supplier_name,
                   p.category, p.price, p.stock_quantity, p.reorder_level
            FROM Products p
            LEFT JOIN Suppliers s ON p.supplier_id = s.supplier_id
            WHERE p.product_name LIKE %s
               OR p.category LIKE %s
               OR s.supplier_name LIKE %s
            ORDER BY p.product_id
        """, (like_pattern, like_pattern, like_pattern))
        rows = cursor.fetchall()
        _print_product_table(rows)
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def update_product():
    print("\n********** UPDATE PRODUCT **********")
    product_id = input_int("Enter Product ID: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT product_name, category, supplier_id, price, reorder_level FROM Products WHERE product_id = %s",
            (product_id,)
        )
        product = cursor.fetchone()
        if not product:
            print(f"\nNo product found with ID {product_id}.")
            return
        name, category, supplier_id, price, reorder = product
        print(f"\nCurrent Product:\n{name}\nCategory: {category}\nSupplier ID: {supplier_id}"
              f"\nPrice: Rs.{price}\nReorder Level: {reorder}")
        print("\nLeave a field blank to keep its current value.")
        new_name = input(f"New name [{name}]: ").strip() or name
        new_category = input(f"New category [{category}]: ").strip() or category
        new_supplier_raw = input(f"New Supplier ID [{supplier_id}]: ").strip()
        new_supplier_id = int(new_supplier_raw) if new_supplier_raw else supplier_id
        if new_supplier_raw:
            cursor.execute("SELECT supplier_id FROM Suppliers WHERE supplier_id = %s", (new_supplier_id,))
            if cursor.fetchone() is None:
                print(f"\nNo supplier found with ID {new_supplier_id}. Update cancelled.")
                return
        new_price_raw = input(f"New price [{price}]: ").strip()
        new_price = float(new_price_raw) if new_price_raw else float(price)
        if new_price < 0:
            print("\nPrice cannot be negative. Update cancelled.")
            return
        new_reorder_raw = input(f"New reorder level [{reorder}]: ").strip()
        new_reorder = int(new_reorder_raw) if new_reorder_raw else reorder
        if new_reorder < 0:
            print("\nReorder level cannot be negative. Update cancelled.")
            return
        cursor.execute(
            """UPDATE Products
               SET product_name = %s, category = %s, supplier_id = %s,
                   price = %s, reorder_level = %s
               WHERE product_id = %s""",
            (new_name, new_category, new_supplier_id, new_price, new_reorder, product_id)
        )
        conn.commit()
        print("\nProduct updated successfully!")
    except Error as err:
        print(f"\n[Database Error] {err}")
        conn.rollback()
    finally:
        conn.close()


def delete_product():
    print("\n********** DELETE PRODUCT **********")
    product_id = input_int("Enter Product ID to delete: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT product_name FROM Products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            print(f"\nNo product found with ID {product_id}.")
            return
        cursor.execute("SELECT COUNT(*) FROM Purchase_Items WHERE product_id = %s", (product_id,))
        purchase_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Sale_Items WHERE product_id = %s", (product_id,))
        sale_count = cursor.fetchone()[0]
        if purchase_count > 0 or sale_count > 0:
            print(f"\nCannot delete '{product[0]}': it has {purchase_count} purchase record(s) "
                  f"and {sale_count} sale record(s). Deleting it would destroy transaction history.")
            return
        if not input_yes_no(f"Are you sure you want to delete '{product[0]}'? (y/n): "):
            print("\nDeletion cancelled.")
            return
        cursor.execute("DELETE FROM Products WHERE product_id = %s", (product_id,))
        conn.commit()
        print("\nProduct deleted successfully!")
    except Error as err:
        print(f"\n[Database Error] {err}")
        conn.rollback()
    finally:
        conn.close()


def add_supplier():
    print("\n********** ADD SUPPLIER **********")
    name = input_nonempty("Supplier name: ")
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    address = input("Address: ").strip()
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Suppliers (supplier_name, phone, email, address) VALUES (%s, %s, %s, %s)",
            (name, phone, email, address)
        )
        conn.commit()
        print(f"\nSupplier added successfully!\nSupplier ID: {cursor.lastrowid}")
    except Error as err:
        print(f"\n[Database Error] {err}")
        conn.rollback()
    finally:
        conn.close()


def view_suppliers():
    print("\n*************** SUPPLIERS ***************")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT supplier_id, supplier_name, phone, email, address FROM Suppliers ORDER BY supplier_id")
        rows = cursor.fetchall()
        if not rows:
            print("No suppliers found.")
            return
        print(f"{'ID':<5}{'Supplier':<25}{'Phone':<15}{'Email':<25}{'Address':<20}")
        print("-" * 90)
        for sid, name, phone, email, address in rows:
            print(f"{sid:<5}{name:<25}{phone or '':<15}{email or '':<25}{address or '':<20}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def update_supplier():
    print("\n********** UPDATE SUPPLIER **********")
    supplier_id = input_int("Enter Supplier ID: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT supplier_name, phone, email, address FROM Suppliers WHERE supplier_id = %s",
                        (supplier_id,))
        supplier = cursor.fetchone()
        if not supplier:
            print(f"\nNo supplier found with ID {supplier_id}.")
            return
        name, phone, email, address = supplier
        print(f"\nCurrent: {name}, {phone}, {email}, {address}")
        print("Leave a field blank to keep its current value.")
        new_name = input(f"New name [{name}]: ").strip() or name
        new_phone = input(f"New phone [{phone}]: ").strip() or phone
        new_email = input(f"New email [{email}]: ").strip() or email
        new_address = input(f"New address [{address}]: ").strip() or address
        cursor.execute(
            "UPDATE Suppliers SET supplier_name=%s, phone=%s, email=%s, address=%s WHERE supplier_id=%s",
            (new_name, new_phone, new_email, new_address, supplier_id)
        )
        conn.commit()
        print("\nSupplier updated successfully!")
    except Error as err:
        print(f"\n[Database Error] {err}")
        conn.rollback()
    finally:
        conn.close()


def delete_supplier():
    print("\n********** DELETE SUPPLIER **********")
    supplier_id = input_int("Enter Supplier ID to delete: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT supplier_name FROM Suppliers WHERE supplier_id = %s", (supplier_id,))
        supplier = cursor.fetchone()
        if not supplier:
            print(f"\nNo supplier found with ID {supplier_id}.")
            return
        cursor.execute("SELECT COUNT(*) FROM Products WHERE supplier_id = %s", (supplier_id,))
        product_count = cursor.fetchone()[0]
        if product_count > 0:
            print(f"\nCannot delete '{supplier[0]}': {product_count} product(s) are linked to this supplier. "
                  f"Reassign or delete those products first.")
            return
        if not input_yes_no(f"Are you sure you want to delete '{supplier[0]}'? (y/n): "):
            print("\nDeletion cancelled.")
            return
        cursor.execute("DELETE FROM Suppliers WHERE supplier_id = %s", (supplier_id,))
        conn.commit()
        print("\nSupplier deleted successfully!")
    except Error as err:
        print(f"\n[Database Error] {err}")
        conn.rollback()
    finally:
        conn.close()


def record_purchase():
    print("\n********** NEW PURCHASE **********")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        supplier_id = input_int("Supplier ID: ")
        cursor.execute("SELECT supplier_id FROM Suppliers WHERE supplier_id = %s", (supplier_id,))
        if cursor.fetchone() is None:
            print(f"\nNo supplier found with ID {supplier_id}. Purchase cancelled.")
            return
        items = [] 
        while True:
            product_id = input_int("\nProduct ID: ")
            cursor.execute("SELECT product_name FROM Products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()
            if not product:
                print(f"No product found with ID {product_id}. Skipping this line.")
                continue
            quantity = input_int("Quantity: ")
            if quantity <= 0:
                print("Quantity must be greater than 0. Skipping this line.")
                continue
            purchase_price = input_float("Purchase Price: ")
            line_total = quantity * purchase_price
            print(f"{product[0]}\n{quantity} x Rs.{purchase_price} = Rs.{line_total}")
            items.append((product_id, quantity, purchase_price, line_total))
            if not input_yes_no("Add another product? (y/n): "):
                break
        if not items:
            print("\nNo items entered. Purchase cancelled.")
            return
        total_amount = sum(item[3] for item in items)
        print(f"\nTotal Purchase Amount: Rs.{total_amount}")
        conn.start_transaction()
        cursor.execute(
            "INSERT INTO Purchases (supplier_id, purchase_date, total_amount) VALUES (%s, %s, %s)",
            (supplier_id, datetime.now(), total_amount)
        )
        purchase_id = cursor.lastrowid
        for product_id, quantity, purchase_price, _ in items:
            cursor.execute(
                "INSERT INTO Purchase_Items (purchase_id, product_id, quantity, purchase_price) VALUES (%s, %s, %s, %s)",
                (purchase_id, product_id, quantity, purchase_price)
            )
            cursor.execute(
                "UPDATE Products SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
                (quantity, product_id)
            )
        conn.commit()
        print(f"\nPurchase recorded successfully!\n\nPurchase ID: {purchase_id}"
              f"\nTotal Amount: Rs.{total_amount}\nStock updated successfully.")
    except Error as err:
        print(f"\n[Database Error] {err}\nRolling back transaction - no changes were saved.")
        conn.rollback()
    finally:
        conn.close()


def view_purchases():
    print("\n*************** PURCHASE REPORT ***************")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT purchase_id, purchase_date, total_amount FROM Purchases ORDER BY purchase_date DESC")
        rows = cursor.fetchall()
        if not rows:
            print("No purchases recorded yet.")
            return
        print(f"{'Purchase ID':<15}{'Date':<22}{'Amount':<10}")
        print("-" * 47)
        for pid, date, amount in rows:
            print(f"{pid:<15}{str(date):<22}Rs.{amount}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def purchase_details():
    print("\n*************** PURCHASE DETAILS ***************")
    purchase_id = input_int("Enter Purchase ID: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT purchase_date, total_amount FROM Purchases WHERE purchase_id = %s", (purchase_id,))
        header = cursor.fetchone()
        if not header:
            print(f"\nNo purchase found with ID {purchase_id}.")
            return
        print(f"\nPurchase ID: {purchase_id}\nDate: {header[0]}\n")
        cursor.execute("""
            SELECT p.product_name, pi.quantity, pi.purchase_price
            FROM Purchase_Items pi
            JOIN Products p ON pi.product_id = p.product_id
            WHERE pi.purchase_id = %s
        """, (purchase_id,))
        items = cursor.fetchall()
        print(f"{'Product':<15}{'Quantity':<12}{'Price':<10}{'Total':<10}")
        print("-" * 47)
        for name, qty, price in items:
            print(f"{name:<15}{qty:<12}Rs.{price:<8}Rs.{qty * float(price)}")
        print("-" * 47)
        print(f"{'Total Amount:':<37}Rs.{header[1]}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def record_sale():
    print("\n********** NEW SALE **********")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        items = []
        while True:
            product_id = input_int("\nProduct ID: ")
            cursor.execute("SELECT product_name, price, stock_quantity FROM Products WHERE product_id = %s",
                            (product_id,))
            product = cursor.fetchone()
            if not product:
                print(f"No product found with ID {product_id}. Skipping this line.")
                continue
            name, price, current_stock = product
            quantity = input_int("Quantity: ")
            if quantity <= 0:
                print("Quantity must be greater than 0. Skipping this line.")
                continue
            if quantity > current_stock:
                print(f"\nInsufficient stock!\nAvailable stock: {current_stock}\nRequested: {quantity}")
                continue
            line_total = quantity * float(price)
            print(f"{name}\n{quantity} x Rs.{price} = Rs.{line_total}")
            items.append((product_id, name, quantity, float(price), line_total))
            if not input_yes_no("Add another product? (y/n): "):
                break
        if not items:
            print("\nNo items entered. Sale cancelled.")
            return
        total_amount = sum(item[4] for item in items)
        print(f"\nTotal: Rs.{total_amount}")
        conn.start_transaction()
        for product_id, name, quantity, price, _ in items:
            cursor.execute("SELECT stock_quantity FROM Products WHERE product_id = %s FOR UPDATE", (product_id,))
            current_stock = cursor.fetchone()[0]
            if quantity > current_stock:
                raise ValueError(
                    f"Insufficient stock for '{name}'. Available: {current_stock}, Requested: {quantity}."
                )
        cursor.execute(
            "INSERT INTO Sales (sale_date, total_amount) VALUES (%s, %s)",
            (datetime.now(), total_amount)
        )
        sale_id = cursor.lastrowid
        for product_id, name, quantity, price, _ in items:
            cursor.execute(
                "INSERT INTO Sale_Items (sale_id, product_id, quantity, selling_price) VALUES (%s, %s, %s, %s)",
                (sale_id, product_id, quantity, price)
            )
            cursor.execute(
                "UPDATE Products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                (quantity, product_id)
            )
        conn.commit()
        print(f"\nSale recorded successfully!\n\nSale ID: {sale_id}\nTotal Amount: Rs.{total_amount}"
              f"\nStock updated successfully.")
    except ValueError as ve:
        print(f"\n{ve}\nRolling back transaction - no changes were saved.")
        conn.rollback()
    except Error as err:
        print(f"\n[Database Error] {err}\nRolling back transaction - no changes were saved.")
        conn.rollback()
    finally:
        conn.close()


def view_sales():
    print("\n*************** SALES REPORT ***************")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT sale_id, sale_date, total_amount FROM Sales ORDER BY sale_date DESC")
        rows = cursor.fetchall()
        if not rows:
            print("No sales recorded yet.")
            return
        print(f"{'Sale ID':<12}{'Date':<22}{'Total':<10}")
        print("-" * 44)
        for sid, date, amount in rows:
            print(f"{sid:<12}{str(date):<22}Rs.{amount}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def sale_details():
    print("\n*************** SALE DETAILS ***************")
    sale_id = input_int("Enter Sale ID: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT sale_date, total_amount FROM Sales WHERE sale_id = %s", (sale_id,))
        header = cursor.fetchone()
        if not header:
            print(f"\nNo sale found with ID {sale_id}.")
            return
        print(f"\nSale ID: {sale_id}\nDate: {header[0]}\n")
        cursor.execute("""
            SELECT p.product_name, si.quantity, si.selling_price
            FROM Sale_Items si
            JOIN Products p ON si.product_id = p.product_id
            WHERE si.sale_id = %s
        """, (sale_id,))
        items = cursor.fetchall()
        print(f"{'Product':<15}{'Quantity':<12}{'Price':<10}{'Total':<10}")
        print("-" * 47)
        for name, qty, price in items:
            print(f"{name:<15}{qty:<12}Rs.{price:<8}Rs.{qty * float(price)}")
        print("-" * 47)
        print(f"{'Total Amount:':<37}Rs.{header[1]}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def view_stock():
    print("\n*************** CURRENT STOCK ***************")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, product_name, stock_quantity, reorder_level FROM Products ORDER BY product_id")
        rows = cursor.fetchall()
        if not rows:
            print("No products found.")
            return
        print(f"{'ID':<5}{'Product':<20}{'Stock':<10}{'Reorder Level':<15}")
        print("-" * 50)
        for pid, name, stock, reorder in rows:
            print(f"{pid:<5}{name:<20}{stock:<10}{reorder:<15}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def update_stock():
    print("\n********** MANUAL STOCK UPDATE **********")
    product_id = input_int("Enter Product ID: ")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, stock_quantity FROM Products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            print(f"\nNo product found with ID {product_id}.")
            return
        print(f"\n{product[0]}\nCurrent stock: {product[1]}")
        new_stock = input_int("Enter new stock quantity: ")
        cursor.execute("UPDATE Products SET stock_quantity = %s WHERE product_id = %s", (new_stock, product_id))
        conn.commit()
        print("\nStock updated successfully!")
    except Error as err:
        print(f"\n[Database Error] {err}")
        conn.rollback()
    finally:
        conn.close()


def low_stock_alert():
    print("\n********** LOW STOCK ALERT **********")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_name, stock_quantity, reorder_level
            FROM Products
            WHERE stock_quantity <= reorder_level
            ORDER BY stock_quantity ASC
        """)
        rows = cursor.fetchall()
        if not rows:
            print("All products are sufficiently stocked.")
            return
        print(f"{'Product':<20}{'Current Stock':<16}{'Reorder Level':<15}")
        print("-" * 51)
        for name, stock, reorder in rows:
            print(f"{name:<20}{stock:<16}{reorder:<15}")
        print("\nWarning: These products need restocking.")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def sales_report():
    view_sales()

def purchase_report():
    view_purchases()

def total_sales():
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total_amount) FROM Sales")
        result = cursor.fetchone()[0] or 0
        print(f"\nTotal Sales: Rs.{result}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def total_purchases():
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total_amount) FROM Purchases")
        result = cursor.fetchone()[0] or 0
        print(f"\nTotal Purchases: Rs.{result}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def product_sales_summary():
    print("\n********** PRODUCT SALES SUMMARY **********")
    conn = connect_database()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.product_name, SUM(si.quantity) AS qty_sold, SUM(si.quantity * si.selling_price) AS revenue
            FROM Sale_Items si
            JOIN Products p ON si.product_id = p.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY revenue DESC
        """)
        rows = cursor.fetchall()
        if not rows:
            print("No sales data available yet.")
            return
        print(f"{'Product':<20}{'Quantity Sold':<16}{'Revenue':<12}")
        print("-" * 48)
        for name, qty, revenue in rows:
            print(f"{name:<20}{qty:<16}Rs.{revenue}")
    except Error as err:
        print(f"\n[Database Error] {err}")
    finally:
        conn.close()


def reports_menu():
    while True:
        print("\n*************** REPORTS ***************")
        print("1. Sales Report")
        print("2. Purchase Report")
        print("3. Low Stock Report")
        print("4. Total Sales")
        print("5. Total Purchases")
        print("6. Product Sales Summary")
        print("7. Back")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            sales_report()
        elif choice == "2":
            purchase_report()
        elif choice == "3":
            low_stock_alert()
        elif choice == "4":
            total_sales()
        elif choice == "5":
            total_purchases()
        elif choice == "6":
            product_sales_summary()
        elif choice == "7":
            break
        else:
            print("\nInvalid choice. Please try again.")


def product_menu():
    while True:
        print("\n********** PRODUCT MANAGEMENT **********")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Products")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Back")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            search_products()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice. Please try again.")


def supplier_menu():
    while True:
        print("\n********** SUPPLIER MANAGEMENT **********")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Update Supplier")
        print("4. Delete Supplier")
        print("5. Back")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            add_supplier()
        elif choice == "2":
            view_suppliers()
        elif choice == "3":
            update_supplier()
        elif choice == "4":
            delete_supplier()
        elif choice == "5":
            break
        else:
            print("\nInvalid choice. Please try again.")


def purchase_menu():
    while True:
        print("\n********** PURCHASE MANAGEMENT **********")
        print("1. Record Purchase")
        print("2. View Purchases")
        print("3. Purchase Details")
        print("4. Back")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            record_purchase()
        elif choice == "2":
            view_purchases()
        elif choice == "3":
            purchase_details()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice. Please try again.")


def sales_menu():
    while True:
        print("\n********** SALES MANAGEMENT **********")
        print("1. Record Sale")
        print("2. View Sales")
        print("3. Sale Details")
        print("4. Back")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            record_sale()
        elif choice == "2":
            view_sales()
        elif choice == "3":
            sale_details()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice. Please try again.")


def stock_menu():
    while True:
        print("\n********** STOCK MANAGEMENT **********")
        print("1. View Stock")
        print("2. Update Stock")
        print("3. Low Stock Alert")
        print("4. Back")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            view_stock()
        elif choice == "2":
            update_stock()
        elif choice == "3":
            low_stock_alert()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice. Please try again.")


def main_menu():
    while True:
        print("\n****************************************")
        print("       INVENTORY MANAGEMENT SYSTEM")
        print("****************************************")
        print("1. Product Management")
        print("2. Supplier Management")
        print("3. Purchase Management")
        print("4. Sales Management")
        print("5. Stock Management")
        print("6. Reports")
        print("7. Exit")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            product_menu()
        elif choice == "2":
            supplier_menu()
        elif choice == "3":
            purchase_menu()
        elif choice == "4":
            sales_menu()
        elif choice == "5":
            stock_menu()
        elif choice == "6":
            reports_menu()
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()

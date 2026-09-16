
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


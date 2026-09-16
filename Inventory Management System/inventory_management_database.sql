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
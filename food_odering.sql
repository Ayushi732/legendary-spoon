CREATE DATABASE food_ordering;

USE food_ordering;

CREATE TABLE menu (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    items VARCHAR(255),
    total DECIMAL(10,2),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample menu items
INSERT INTO menu (item_name, price) VALUES
('Pizza', 199.00),
('Burger', 99.00),
('Pasta', 149.00),
('Sandwich', 79.00),
('Cold Coffee', 89.00),
('French Fries', 59.00);



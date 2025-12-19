USE demo_db;

-- 기존 users 테이블 (유지)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--  Debezium용 유저 생성 및 권한 부여
CREATE USER 'debezium'@'%' IDENTIFIED BY 'dbz';
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'debezium'@'%';
FLUSH PRIVILEGES;

-- 1. 상품 테이블 (기초 데이터)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock INT DEFAULT 100
);

-- 2. 주문 테이블 (핵심 트랜잭션)
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT,
    total_price DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, SHIPPED, CANCELLED
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);


-- 기초 상품 데이터 몇 개 넣어두기
INSERT INTO products (name, category, price) VALUES 
('Gaming Mouse', 'Electronics', 59.99),
('Mechanical Keyboard', 'Electronics', 129.50),
('Coffee Mug', 'Home', 12.00),
('Hoodie', 'Apparel', 45.00),
('USB-C Cable', 'Electronics', 9.99);

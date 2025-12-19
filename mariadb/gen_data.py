import mysql.connector
import time
import random
from faker import Faker
from datetime import datetime

# DB 설정 (Localhost -> Docker MariaDB)
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',       # 또는 user
    'password': 'root',   # 또는 userpw (docker-compose 설정 따름)
    'database': 'demo_db'
}

fake = Faker()

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def generate_traffic():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🚀 Starting Traffic Generator... (Press Ctrl+C to stop)")
    
    try:
        while True:
            action = random.choices(['INSERT', 'UPDATE', 'DELETE'], weights=[70, 20, 10])[0]
            
            if action == 'INSERT':
                # 1. 새 유저 생성 (가끔)
                if random.random() < 0.2:
                    name = fake.name()
                    email = fake.email()
                    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
                    print(f"[USER] Created: {name}")

                # 2. 주문 생성 (자주)
                # 랜덤 유저와 상품 ID 가져오기
                cursor.execute("SELECT id FROM users ORDER BY RAND() LIMIT 1")
                user = cursor.fetchone()
                cursor.execute("SELECT id, price FROM products ORDER BY RAND() LIMIT 1")
                product = cursor.fetchone()

                if user and product:
                    u_id = user[0]
                    p_id, price = product
                    qty = random.randint(1, 5)
                    total = float(price) * qty
                    
                    sql = """INSERT INTO orders (user_id, product_id, quantity, total_price, status) 
                             VALUES (%s, %s, %s, %s, 'PENDING')"""
                    cursor.execute(sql, (u_id, p_id, qty, total))
                    print(f"[ORDER] New Order! User {u_id} bought Item {p_id} ($ {total})")

            elif action == 'UPDATE':
                # 주문 상태 변경 (PENDING -> SHIPPED)
                cursor.execute("SELECT id FROM orders WHERE status='PENDING' ORDER BY RAND() LIMIT 1")
                target = cursor.fetchone()
                if target:
                    cursor.execute("UPDATE orders SET status='SHIPPED' WHERE id=%s", (target[0],))
                    print(f"[UPDATE] Order {target[0]} status changed to SHIPPED")

            elif action == 'DELETE':
                # 주문 취소 (데이터 삭제)
                cursor.execute("SELECT id FROM orders ORDER BY RAND() LIMIT 1")
                target = cursor.fetchone()
                if target:
                    cursor.execute("DELETE FROM orders WHERE id=%s", (target[0],))
                    print(f"[DELETE] Order {target[0]} was cancelled (Deleted)")

            conn.commit()
            
            # 속도 조절 (0.5초 ~ 2초 사이 랜덤 대기)
            sleep_time = random.uniform(0.5, 2.0)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n🛑 Stopping generator...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_traffic()

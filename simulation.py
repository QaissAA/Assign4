import psycopg2
import random
import time
from datetime import datetime

# --- Параметры подключения ---
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "1234"

# --- Соединение с PostgreSQL ---
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
conn.autocommit = False
cur = conn.cursor()

# --- Создание тестовой таблицы для вставки данных ---
cur.execute("""
CREATE TABLE IF NOT EXISTS simulated_activity (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    value INTEGER
)
""")
conn.commit()

# --- Функция вставки случайных данных ---
def insert_random_data():
    now = datetime.now()
    value = random.randint(1, 1000)
    try:
        cur.execute("INSERT INTO simulated_activity (created_at, value) VALUES (%s, %s)", (now, value))
        # случайно делаем коммит или откат, чтобы метрики xact_commit и xact_rollback менялись
        if random.random() < 0.8:
            conn.commit()
            print(f" Inserted value {value}, committed")
        else:
            conn.rollback()
            print(f" Inserted value {value}, rolled back")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting data: {e}")

# --- Основной цикл ---
try:
    while True:
        insert_random_data()
        # ждём случайное время между вставками, чтобы нагрузка была "живой"
        time.sleep(random.randint(5, 20))
except KeyboardInterrupt:
    print("Stopped manually")
finally:
    cur.close()
    conn.close()

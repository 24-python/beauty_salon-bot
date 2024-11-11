import sqlite3
from config import DB_NAME

def get_connection():
    """Создание подключения к базе данных."""
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Создание таблицы мастеров
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS masters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialty TEXT
    )
    ''')

    # Создание таблицы услуг
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        duration INTEGER,
        price REAL,
        master_id INTEGER,
        FOREIGN KEY (master_id) REFERENCES masters(id)
    )
    ''')

    # Создание таблицы записей клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        service_id INTEGER,
        appointment_date TEXT,
        master_id INTEGER,
        FOREIGN KEY (service_id) REFERENCES services(id),
        FOREIGN KEY (master_id) REFERENCES masters(id)
    )
    ''')

    conn.commit()
    conn.close()

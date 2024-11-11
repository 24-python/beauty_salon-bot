from database import get_connection

def add_master(name, specialty):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO masters (name, specialty) VALUES (?, ?)', (name, specialty))
    conn.commit()
    conn.close()

def add_service(name, duration, price, master_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO services (name, duration, price, master_id) VALUES (?, ?, ?, ?)',
                   (name, duration, price, master_id))
    conn.commit()
    conn.close()

def view_masters():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM masters')
    masters = cursor.fetchall()
    conn.close()
    return masters

def view_services():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM services')
    services = cursor.fetchall()
    conn.close()
    return services

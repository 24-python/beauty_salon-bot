from database import get_connection

def book_appointment(client_name, service_id, appointment_date):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT master_id FROM services WHERE id = ?', (service_id,))
    master_id = cursor.fetchone()
    
    if master_id:
        cursor.execute('''
            INSERT INTO appointments (client_name, service_id, appointment_date, master_id) 
            VALUES (?, ?, ?, ?)
        ''', (client_name, service_id, appointment_date, master_id[0]))
        conn.commit()
        print(f'Запись для {client_name} успешно добавлена на {appointment_date}')
    else:
        print('Услуга не найдена')
    
    conn.close()

def view_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT a.id, a.client_name, s.name, a.appointment_date, m.name 
    FROM appointments a
    JOIN services s ON a.service_id = s.id
    JOIN masters m ON a.master_id = m.id
    ''')
    appointments = cursor.fetchall()
    conn.close()
    return appointments

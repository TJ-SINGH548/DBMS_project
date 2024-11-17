import sqlite3 as sq

conn = sq.connect('patient_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE patient(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        aadhar BLOB
    )
''')

cursor.execute('''
    CREATE TABLE doctor(
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT,
        license_number TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE Appointments(
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patient(id),
        FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
    )
''')

cursor.execute('''
    CREATE TABLE medical_history(
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        medical_records TEXT NOT NULL,
        allergies TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patient(id),
        FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
    )
''')

cursor.execute('''
    CREATE TABLE medical_records(
        patient_id INTEGER NOT NULL,
        patient_history_records TEXT,
        diagnosis TEXT NOT NULL,
        date TEXT NOT NULL,
        treatment TEXT NOT NULL,
        allergies TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patient(id)
    )
''')

conn.commit()
conn.close()

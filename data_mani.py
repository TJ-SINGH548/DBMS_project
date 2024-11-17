import sqlite3 as sq
import pandas as pd

conn = sq.connect('patient_database.db')
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO patient (name, age, gender, address, phone, aadhar)
    VALUES (?, ?, ?, ?, ?, ?)
''', ('Chunchun', 21, 'Male', 'A-22 Sun Quaters', '8928075088', None))

patient_id = cursor.lastrowid

cursor.execute('''
    INSERT INTO doctor (name, specialty, phone, email, address, license_number)
    VALUES (?, ?, ?, ?, ?, ?)
''', ('Dr. Smith', 'Cardiology', '555-1234', 'drsmith@example.com', '101 Health St', 'ABC123456'))

doctor_id = cursor.lastrowid

cursor.execute('''
    INSERT INTO Appointments (patient_id, doctor_id, date, status)
    VALUES (?, ?, ?, ?)
''', (patient_id, doctor_id, '2024-10-15', 'healthy'))

cursor.execute('''
    INSERT INTO medical_history (patient_id, doctor_id, medical_records, allergies)
    VALUES (?, ?, ?, ?)
''', (patient_id, doctor_id, 'Routine checkup', 'None'))

cursor.execute('''
    INSERT INTO medical_records (patient_id, patient_history_records, diagnosis, date, treatment, allergies)
    VALUES (?, ?, ?, ?, ?, ?)
''', (patient_id, 'No significant medical history', 'Healthy', '2024-10-15', 'N/A', 'None'))

conn.commit()

patient_data = {
    'patient_id': [patient_id],
    'name': ['Chunchun'],
    'age': [21],
    'gender': ['Male'],
    'address': ['A-22 Sun Quaters'],
    'phone': ['8928075088'],
    'aadhar': [None]
}
patient_df = pd.DataFrame(patient_data)
patient_df.to_csv('patient_data.csv', mode='a', header=False, index=False)

doctor_data = {
    'doctor_id': [doctor_id],
    'name': ['Dr. Smith'],
    'specialty': ['Cardiology'],
    'phone': ['555-1234'],
    'email': ['drsmith@example.com'],
    'address': ['101 Health St'],
    'license_number': ['ABC123456']
}
doctor_df = pd.DataFrame(doctor_data)
doctor_df.to_csv('doctor_data.csv', mode='a', header=False, index=False)

appointment_data = {
    'appointment_id': [None],
    'patient_id': [patient_id],
    'doctor_id': [doctor_id],
    'date': ['2024-10-15'],
    'status': ['healthy']
}
appointment_df = pd.DataFrame(appointment_data)
appointment_df.to_csv('appointment_data.csv', mode='a', header=False, index=False)

medical_history_data = {
    'patient_id': [patient_id],
    'doctor_id': [doctor_id],
    'medical_records': ['Routine checkup'],
    'allergies': ['None']
}
medical_history_df = pd.DataFrame(medical_history_data)
medical_history_df.to_csv('medical_history_data.csv', mode='a', header=False, index=False)

medical_records_data = {
    'patient_id': [patient_id],
    'patient_history_records': ['No significant medical history'],
    'diagnosis': ['Healthy'],
    'date': ['2024-10-15'],
    'treatment': ['N/A'],
    'allergies': ['None']
}
medical_records_df = pd.DataFrame(medical_records_data)
medical_records_df.to_csv('medical_records_data.csv', mode='a', header=False, index=False)

conn.close()

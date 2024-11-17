import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime, timedelta

class DatabaseTriggers:
    def __init__(self, db_path='patient_database.db'):
        self.db_path = db_path
        self.setup_triggers()
    
    def setup_triggers(self):
        conn = sq.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create triggers
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS after_appointment_insert
            AFTER INSERT ON Appointments
            BEGIN
                INSERT INTO medical_records (
                    patient_id, 
                    patient_history_records,
                    diagnosis,
                    date,
                    treatment,
                    allergies
                )
                VALUES (
                    NEW.patient_id,
                    'New appointment created',
                    'Pending',
                    NEW.date,
                    'Pending',
                    'To be updated'
                );
            END;
        ''')

        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS check_appointment_overlap
            BEFORE INSERT ON Appointments
            BEGIN
                SELECT CASE
                    WHEN EXISTS (
                        SELECT 1 FROM Appointments
                        WHERE doctor_id = NEW.doctor_id
                        AND date = NEW.date
                    )
                    THEN RAISE (ABORT, 'Doctor already has an appointment at this time')
                END;
            END;
        ''')

        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_medical_history
            AFTER UPDATE ON medical_records
            BEGIN
                INSERT INTO medical_history (
                    patient_id,
                    doctor_id,
                    medical_records,
                    allergies
                )
                SELECT
                    NEW.patient_id,
                    (SELECT doctor_id FROM Appointments WHERE patient_id = NEW.patient_id ORDER BY date DESC LIMIT 1),
                    NEW.patient_history_records || ' | ' || NEW.diagnosis,
                    NEW.allergies;
            END;
        ''')
        
        conn.commit()
        conn.close()

    def create_appointment_reminder(self):
        conn = sq.connect(self.db_path)
        cursor = conn.cursor()
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT p.name, p.phone, a.date
            FROM Appointments a
            JOIN patient p ON a.patient_id = p.id
            WHERE a.date = ?
        ''', (tomorrow,))
        
        reminders = cursor.fetchall()
        conn.close()
        
        if reminders:
            messagebox.showinfo("Appointment Reminders", 
                              f"Appointments tomorrow ({tomorrow}):\n" + 
                              "\n".join([f"Patient: {r[0]}, Phone: {r[1]}" for r in reminders]))
        return reminders

    def check_appointment_status(self):
        conn = sq.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.name, a.date, a.status
            FROM Appointments a
            JOIN patient p ON a.patient_id = p.id
            WHERE a.status != 'completed'
            AND date(a.date) < date('now')
        ''')
        
        pending_appointments = cursor.fetchall()
        conn.close()
        
        if pending_appointments:
            messagebox.showwarning("Pending Appointments", 
                                 "Past appointments need status update:\n" + 
                                 "\n".join([f"Patient: {r[0]}, Date: {r[1]}" for r in pending_appointments]))
        return pending_appointments

    def analyze_patient_visits(self):
        conn = sq.connect(self.db_path)
        
        query = '''
            SELECT 
                p.name,
                COUNT(a.appointment_id) as visit_count,
                GROUP_CONCAT(DISTINCT m.diagnosis) as diagnoses
            FROM patient p
            LEFT JOIN Appointments a ON p.id = a.patient_id
            LEFT JOIN medical_records m ON p.id = m.patient_id
            GROUP BY p.id
            HAVING visit_count > 1
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            messagebox.showinfo("Patient Visit Analysis",
                              "Frequent Visitors:\n" + 
                              df.to_string())
        return df

def integrate_with_gui(root):
    triggers = DatabaseTriggers()
    
    # Create a new frame for trigger buttons
    trigger_frame = tk.Frame(root)
    trigger_frame.pack(side=tk.RIGHT, padx=10, pady=10)
    
    # Add buttons for each trigger function
    tk.Button(trigger_frame, 
              text="Check Tomorrow's Appointments",
              command=triggers.create_appointment_reminder).pack(pady=5)
    
    tk.Button(trigger_frame,
              text="Check Pending Appointments",
              command=triggers.check_appointment_status).pack(pady=5)
    
    tk.Button(trigger_frame,
              text="Patient Visit Analysis",
              command=triggers.analyze_patient_visits).pack(pady=5)

if __name__ == "__main__":
    # Test the triggers
    triggers = DatabaseTriggers()
    
    # Create a test GUI window
    root = tk.Tk()
    root.title("Database Triggers Test")
    integrate_with_gui(root)
    root.mainloop()
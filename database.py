import sqlite3


DATABASE_NAME = "appointments.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Confirmed'
        )
    """)

    connection.commit()

    connection.close()


def add_appointment(
    patient_name,
    phone,
    department,
    doctor,
    appointment_date,
    appointment_time
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO appointments
        (
            patient_name,
            phone,
            department,
            doctor,
            appointment_date,
            appointment_time,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_name,
        phone,
        department,
        doctor,
        str(appointment_date),
        str(appointment_time),
        "Confirmed"
    ))

    connection.commit()

    connection.close()


def get_appointments():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            patient_name,
            phone,
            department,
            doctor,
            appointment_date,
            appointment_time,
            status
        FROM appointments
        ORDER BY id DESC
    """)

    appointments = cursor.fetchall()

    connection.close()

    return appointments


def appointment_exists(
    doctor,
    appointment_date,
    appointment_time
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM appointments
        WHERE doctor = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND status = 'Confirmed'
    """, (
        doctor,
        str(appointment_date),
        str(appointment_time)
    ))

    appointment = cursor.fetchone()

    connection.close()

    return appointment is not None


# ============================================================
# GET BOOKED TIME SLOTS
# ============================================================

def get_booked_times(
    doctor,
    appointment_date
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT appointment_time
        FROM appointments
        WHERE doctor = ?
        AND appointment_date = ?
        AND status = 'Confirmed'
    """, (
        doctor,
        str(appointment_date)
    ))

    booked_times = cursor.fetchall()

    connection.close()

    return [
        time[0]
        for time in booked_times
    ]


def cancel_appointment(appointment_id):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE appointments
        SET status = 'Cancelled'
        WHERE id = ?
    """, (appointment_id,))

    connection.commit()

    connection.close()


# Create database when the program starts
create_database()
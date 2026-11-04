import sqlite3


DATABASE_NAME = "appointments.db"


connection = sqlite3.connect(DATABASE_NAME)

cursor = connection.cursor()


# ============================================================
# CHECK AND ADD STATUS COLUMN
# ============================================================

try:

    cursor.execute("""
        ALTER TABLE appointments
        ADD COLUMN status TEXT NOT NULL DEFAULT 'Confirmed'
    """)

    connection.commit()

    print("Database updated successfully!")
    print("Status column added.")


except sqlite3.OperationalError as error:

    if "duplicate column name" in str(error):

        print("Status column already exists.")
        print("No database changes are required.")

    else:

        print("Database update error:")
        print(error)


# ============================================================
# CHECK DATABASE STRUCTURE
# ============================================================

cursor.execute("""
    PRAGMA table_info(appointments)
""")

columns = cursor.fetchall()


print()
print("====================================")
print("APPOINTMENTS TABLE")
print("====================================")

for column in columns:

    column_id = column[0]
    column_name = column[1]
    data_type = column[2]

    print(
        f"{column_id}. {column_name} ({data_type})"
    )


connection.close()


print()
print("Database connection closed.")
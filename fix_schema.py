import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="campus_connect"
    )
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE document_requests MODIFY COLUMN status VARCHAR(100) DEFAULT 'Pending HOD'")
    conn.commit()
    print("Successfully updated document_requests table status column.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")

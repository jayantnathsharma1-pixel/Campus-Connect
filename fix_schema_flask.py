from app import app, mysql

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute("ALTER TABLE document_requests MODIFY COLUMN status VARCHAR(100) DEFAULT 'Pending HOD'")
    mysql.connection.commit()
    print("Successfully updated document_requests table status column!")

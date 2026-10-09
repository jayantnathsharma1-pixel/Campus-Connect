from app import app, mysql

with app.app_context():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("ALTER TABLE requests ADD COLUMN student_hidden BOOLEAN DEFAULT FALSE")
        print("Added student_hidden column.")
    except Exception as e:
        print(f"Column may already exist or error: {e}")
        
    try:
        cursor.execute("ALTER TABLE requests MODIFY COLUMN status VARCHAR(50) DEFAULT 'pending'")
        print("Modified status column to VARCHAR(50).")
    except Exception as e:
        print(f"Error modifying status: {e}")

    mysql.connection.commit()
    cursor.close()
    print("Database updated successfully!")

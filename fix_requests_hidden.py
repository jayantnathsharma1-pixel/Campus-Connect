from app import app, mysql

with app.app_context():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("ALTER TABLE requests ADD COLUMN teacher_hidden BOOLEAN DEFAULT FALSE")
        print("Added teacher_hidden")
    except Exception as e:
        print(e)
    try:
        cursor.execute("ALTER TABLE requests ADD COLUMN admin_hidden BOOLEAN DEFAULT FALSE")
        print("Added admin_hidden")
    except Exception as e:
        print(e)
    mysql.connection.commit()
    cursor.close()
    print("Done")

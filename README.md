# 🎓 Campus Connect – Smart Campus Management System

**One Platform, One Connected Campus**

Campus Connect is a smart campus management web application developed to simplify academic activities, administrative tasks, and communication within educational institutions. It provides a centralized platform for students, teachers, accountants, librarians, and administrators to manage campus-related information efficiently.

The project aims to reduce paperwork, improve communication, and create a more organized and digitally connected campus environment.

## 🚀 Features

### 👨‍🎓 Student Dashboard

* View academic information and student records.
* Access attendance and timetable information.
* Manage campus-related requests.
* Access relevant announcements and updates.

### 👨‍🏫 Teacher Dashboard

* Access teaching-related information.
* Manage academic activities and student information.
* Share announcements and updates.

### 🛡️ Admin Dashboard

* Manage campus users and records.
* Monitor requests and complaints.
* Oversee campus activities and information.

### 💰 Accountant Dashboard

* Manage fee-related information.
* Access accounting and financial records.

### 📚 Librarian Dashboard

* Manage library-related information.
* Support library record management.

### 🔐 Authentication and Account Management

* User registration and login.
* Forgot password and password reset pages.
* OTP verification pages.
* Role-based dashboard access.

### 📄 Additional Functionality

* Certificate printing page.
* Centralized database structure.
* Organized templates and static resources.

## 🛠️ Technology Stack

| Technology | Purpose                       |
| ---------- | ----------------------------- |
| Python     | Backend programming           |
| Flask      | Web application framework     |
| HTML5      | Web page structure            |
| CSS3       | Styling and responsive design |
| JavaScript | Frontend interactivity        |
| MySQL      | Database management           |
| SQL        | Database schema and queries   |

## 📁 Project Structure

```text
campus_connect/
│
├── app.py
├── database.sql
├── .env
├── .gitignore
├── README.md
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── other static resources
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student-dashboard.html
│   ├── teacher-dashboard.html
│   ├── admin-dashboard.html
│   ├── accountant-dashboard.html
│   ├── librarian-dashboard.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── verify_otp.html
│   ├── verify_login_otp.html
│   └── print_certificate.html
│
└── requirements.txt
```

*Note: The static subfolders shown above are examples. Adjust the structure to match your actual files.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/campus-connect-system.git
```

Navigate to the project directory:

```bash
cd campus-connect-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages required by your application. For example:

```bash
pip install Flask python-dotenv
```

Install any additional packages your `app.py` imports, including the MySQL connector or email/OTP libraries if used.

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
FLASK_APP=app.py
FLASK_DEBUG=0
SECRET_KEY=your_secret_key

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=campus_connect
```

Replace the example values with your local configuration. Keep `.env` private and never upload it to GitHub.

### 5. Set Up the MySQL Database

1. Start your MySQL server.
2. Open MySQL Workbench or your preferred MySQL client.
3. Create the database and import the SQL file according to your existing schema.

For example, if `database.sql` contains the database creation statement, execute:

```sql
SOURCE database.sql;
```

Run this command from the appropriate MySQL client and directory. Ensure the database name and credentials match your `.env` configuration.

### 6. Run the Application

From the project root, execute:

```bash
python app.py
```

If the application starts successfully, open the local URL shown in your terminal, usually:

```text
http://127.0.0.1:5000/
```

## 🔒 Security

* Store passwords, secret keys, and database credentials in environment variables.
* Keep `.env` excluded from Git using `.gitignore`.
* Use appropriate password hashing and session security.
* Restrict dashboard access according to user roles.
* Do not publish real student information or sensitive database records.

## 🎯 Project Objectives

* Digitize campus management activities.
* Improve communication between students, teachers, and administrators.
* Simplify academic and administrative workflows.
* Organize accounting and library records.
* Provide a centralized and user-friendly campus platform.

## 🔮 Future Enhancements

* Mobile application integration.
* Email and real-time notifications.
* Online fee payment integration.
* Advanced attendance analytics.
* Enhanced library book tracking.
* Cloud deployment and improved accessibility.

## 👥 Project Information

**Project Name:** Campus Connect – Smart Campus Management System

**Project Type:** Web Application

**Domain:** Education Technology / Smart Campus

**Developed By:** Campus Connect Project Team

**Purpose:** Academic project and smart campus management solution.

## 📜 License

This project is intended for educational and development purposes. Add a suitable open-source license if you plan to distribute or reuse the project publicly.

---

**Campus Connect – One Platform, One Connected Campus.**

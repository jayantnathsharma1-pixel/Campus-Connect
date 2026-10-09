from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import random
import os
import qrcode
import base64
from io import BytesIO
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'campus_connect_hackathon_final_2026')

# =========================================
# FILE UPLOAD CONFIGURATION
# =========================================
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =========================================
# MYSQL CONFIGURATION
# =========================================
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'campus_connect')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

# =========================================
# GMAIL SMTP CONFIGURATION
# =========================================
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('Campus Connect Administration', os.getenv('MAIL_DEFAULT_SENDER_EMAIL', 'jayantnathsharma1@gmail.com'))

mail = Mail(app)

BRANCHES = ['CSE', 'CIVIL', 'ME', 'EE', 'ECE']
YEARS = ['1st Year', '2nd Year', '3rd Year', '4th Year']
DAYS_LIST = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

COMMON_FIRST_YEAR = [
    'Engineering Mathematics-I',
    'Engineering Physics',
    'Programming in C',
    'Basic Electrical Engineering',
    'Engineering Graphics & Design',
    'Environmental Science'
]

SYLLABUS = {
    'CSE': {
        '1st Year': COMMON_FIRST_YEAR,
        '2nd Year': [
            'Data Structures & Algorithms',
            'Database Management Systems',
            'Object Oriented Programming (Java)',
            'Digital Logic Design',
            'Discrete Mathematics',
            'Computer Organization & Architecture'
        ],
        '3rd Year': [
            'Operating Systems',
            'Computer Networks',
            'Software Engineering',
            'Theory of Computation',
            'Web Technologies',
            'Design & Analysis of Algorithms'
        ],
        '4th Year': [
            'Artificial Intelligence & ML',
            'Cloud Computing',
            'Cyber Security & Cryptography',
            'Big Data Analytics',
            'Internet of Things (IoT)',
            'Major Project & Seminar'
        ]
    },
    'CIVIL': {
        '1st Year': COMMON_FIRST_YEAR,
        '2nd Year': [
            'Building Materials & Construction',
            'Strength of Materials',
            'Surveying & Geomatics',
            'Fluid Mechanics',
            'Engineering Geology',
            'Civil Engineering Drawing'
        ],
        '3rd Year': [
            'Structural Analysis',
            'Design of Concrete Structures',
            'Geotechnical Engineering',
            'Hydrology & Water Resources',
            'Transportation Engineering',
            'Environmental Engineering'
        ],
        '4th Year': [
            'Design of Steel Structures',
            'Construction Planning & Management',
            'Earthquake Engineering',
            'Bridge Engineering',
            'Town Planning & Architecture',
            'Major Project & Field Work'
        ]
    },
    'ME': {
        '1st Year': COMMON_FIRST_YEAR,
        '2nd Year': [
            'Engineering Thermodynamics',
            'Strength of Materials',
            'Manufacturing Processes',
            'Material Science & Metallurgy',
            'Kinematics of Machinery',
            'Machine Drawing'
        ],
        '3rd Year': [
            'Dynamics of Machines',
            'Fluid Mechanics & Hydraulic Machinery',
            'Design of Machine Elements',
            'Heat & Mass Transfer',
            'Applied Thermodynamics (IC Engines)',
            'Metrology & Quality Control'
        ],
        '4th Year': [
            'CAD/CAM & Automation',
            'Automobile Engineering',
            'Refrigeration & Air Conditioning',
            'Power Plant Engineering',
            'Robotics & Industrial Automation',
            'Major Capstone Project'
        ]
    },
    'EE': {
        '1st Year': COMMON_FIRST_YEAR,
        '2nd Year': [
            'Circuit Theory & Networks',
            'Electrical Machines - I',
            'Analog Electronics',
            'Electromagnetic Field Theory',
            'Electrical Measurements & Measuring Instruments',
            'Signals & Systems'
        ],
        '3rd Year': [
            'Electrical Machines - II',
            'Control Systems Engineering',
            'Power System Generation & Transmission',
            'Power Electronics',
            'Microprocessors & Microcontrollers',
            'Renewable Energy Systems'
        ],
        '4th Year': [
            'Power System Operation & Control',
            'Electric Drives & Traction',
            'High Voltage Engineering',
            'Switchgear & Protection',
            'Smart Grid Technology',
            'Major Electrical Project'
        ]
    },
    'ECE': {
        '1st Year': COMMON_FIRST_YEAR,
        '2nd Year': [
            'Electronic Devices & Circuits',
            'Digital System Design',
            'Network Analysis & Synthesis',
            'Signals & Systems',
            'Electromagnetic Waves & Transmission Lines',
            'Electronic Measurements'
        ],
        '3rd Year': [
            'Analog & Digital Communication',
            'Microprocessors & Microcontrollers',
            'Linear Integrated Circuits',
            'Control Systems',
            'VLSI Design',
            'Digital Signal Processing'
        ],
        '4th Year': [
            'Wireless & Mobile Communication',
            'Optical Fiber Communication',
            'Embedded Systems & IoT',
            'Radar & Satellite Communication',
            'Antenna & Wave Propagation',
            'Major Capstone Project'
        ]
    }
}

DESIGNATIONS = [
    'Teacher / Professor',
    'Head of Department (HOD)',
    'Principal',
    'Examination Cell / Controller',
    'Hostel Warden',
    'Library Staff / Librarian',
    'Accountant / Clerk',
    'Electrician',
    'Sweeper / Housekeeping',
    'Lab Assistant'
]

def send_otp_email(target_email, user_name, otp, purpose="Verification"):
    try:
        msg = Message(
            subject=f"Campus Connect - OTP for {purpose}",
            recipients=[target_email]
        )
        msg.body = f"""Hello {user_name},

Your 6-digit verification code (OTP) for {purpose} is:

======================
{otp}
======================

Please enter this verification code to complete your admission, onboarding, or authority registration.

Regards,
Campus Connect Security Operations
"""
        mail.send(msg)
        print(f"📧 [EMAIL OTP] Successfully dispatched OTP {otp} to {target_email} ({purpose})")
        return True
    except Exception as e:
        print(f"❌ Error sending email to {target_email}: {e}")
        print(f"🔑 [DEV/LOCAL OTP FALLBACK] OTP for {target_email} ({purpose}) is: {otp}")
        return False

def get_or_create_timetable(cursor, branch, year):
    cursor.execute("""
        SELECT * FROM timetables 
        WHERE branch = %s AND year = %s 
        ORDER BY FIELD(day_name, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
    """, (branch, year))
    rows = cursor.fetchall()

    if not rows:
        subs = SYLLABUS.get(branch, {}).get(year, COMMON_FIRST_YEAR)
        for i, day in enumerate(WEEKDAYS):
            rotated_subs = [subs[(i + offset) % len(subs)] for offset in range(6)]
            cursor.execute("""
                INSERT INTO timetables (branch, year, day_name, period1, period2, period3, period4, period5, period6)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (branch, year, day, rotated_subs[0], rotated_subs[1], rotated_subs[2], rotated_subs[3], rotated_subs[4], rotated_subs[5]))
        mysql.connection.commit()

        cursor.execute("""
            SELECT * FROM timetables 
            WHERE branch = %s AND year = %s 
            ORDER BY FIELD(day_name, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
        """, (branch, year))
        rows = cursor.fetchall()

    return rows

@app.route('/send-onboard-otp', methods=['POST'])
def send_onboard_otp():
    email = request.form.get('email', '').strip().lower()
    name = request.form.get('name', 'Applicant').strip()

    if not email:
        return jsonify({'success': False, 'message': 'Please enter email address first!'})

    otp = str(random.randint(100000, 999999))
    session['onboard_otp'] = otp
    session['onboard_email'] = email

    sent = send_otp_email(email, name, otp, "Email Verification")
    if sent:
        return jsonify({'success': True, 'message': f'OTP sent successfully to {email}!'})
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP email. Please check SMTP credentials.'})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM colleges ORDER BY id ASC")
    colleges = cursor.fetchall()

    if request.method == 'POST':
        college_id = request.form.get('college_id', 'kmbb1234').strip()
        role = request.form.get('role')
        user_id = request.form.get('userId', '').strip()
        password = request.form.get('password', '')

        cursor.execute("""
            SELECT u.*, c.college_name 
            FROM users u 
            LEFT JOIN colleges c ON u.college_id = c.college_id 
            WHERE u.user_id = %s AND u.role = %s AND (u.college_id = %s OR u.college_id IS NULL)
        """, (user_id, role, college_id))
        user = cursor.fetchone()

        if user and user['password'] == password:
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = user['role']
            session['college_id'] = user.get('college_id') or 'kmbb1234'
            session['college_name'] = user.get('college_name') or 'KMBB College of Engineering and Technology'
            session['branch'] = user.get('branch', 'CSE')
            session['year'] = user.get('year', '1st Year')
            session['designation'] = user.get('designation', '')

            flash(f"Welcome back to {session['college_name']}, {user['name']}!", 'success')
            cursor.close()

            if role == 'student':
                return redirect(url_for('student_dashboard'))
            elif role == 'teacher':
                if session['designation'] == 'Library Staff / Librarian':
                    return redirect(url_for('librarian_dashboard'))
                elif session['designation'] == 'Accountant / Clerk':
                    return redirect(url_for('accountant_dashboard'))
                return redirect(url_for('teacher_dashboard'))
            elif role == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid College, Role, User ID, or Password!', 'error')

    cursor.close()
    return render_template('login.html', colleges=colleges)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        branch = request.form.get('branch', 'CSE').strip()
        year = request.form.get('year', '1st Year').strip()
        user_id = request.form.get('userId', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not name or not user_id or not email or not password:
            flash('❌ All fields are required!', 'error')
            return render_template('register.html', branches=BRANCHES, years=YEARS)

        if password != confirm_password:
            flash('❌ Passwords do not match!', 'error')
            return render_template('register.html', branches=BRANCHES, years=YEARS)

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s OR email = %s", (user_id, email))
        existing = cursor.fetchone()
        cursor.close()

        if existing:
            flash('❌ Roll Number/User ID or Email is already registered!', 'error')
            return render_template('register.html', branches=BRANCHES, years=YEARS)

        otp = str(random.randint(100000, 999999))
        session['reg_data'] = {
            'name': name,
            'branch': branch,
            'year': year,
            'user_id': user_id,
            'email': email,
            'password': password,
            'otp': otp
        }

        send_otp_email(email, name, otp, "Student Registration")
        flash(f'📩 Verification OTP sent to {email}. Please enter the code below.', 'success')
        return redirect(url_for('verify_otp'))

    return render_template('register.html', branches=BRANCHES, years=YEARS)

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    reg_data = session.get('reg_data')
    if not reg_data:
        flash('Session expired or invalid registration attempt. Please register again.', 'error')
        return redirect(url_for('register'))

    if request.method == 'POST':
        entered_otp = request.form.get('otp', '').strip()
        if entered_otp != reg_data.get('otp'):
            flash('❌ Invalid OTP! Please check your code.', 'error')
            return render_template('verify_otp.html', title="Student Verification", action_url=url_for('verify_otp'))

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, name, email, role, password, status, branch, year, college_id)
            VALUES (%s, %s, %s, 'student', %s, 'approved', %s, %s, 'kmbb1234')
        """, (reg_data['user_id'], reg_data['name'], reg_data['email'], reg_data['password'], reg_data['branch'], reg_data['year']))
        mysql.connection.commit()
        cursor.close()

        # Auto-login the new student directly
        session['user_id'] = reg_data['user_id']
        session['name'] = reg_data['name']
        session['role'] = 'student'
        session['college_id'] = 'kmbb1234'
        session['college_name'] = 'KMBB College of Engineering and Technology'
        session['branch'] = reg_data['branch']
        session['year'] = reg_data['year']
        session['designation'] = ''

        session.pop('reg_data', None)
        flash('🎉 Registration successful! Welcome to the student portal.', 'success')
        return redirect(url_for('student_dashboard'))

    return render_template('verify_otp.html', title="Student Verification", action_url=url_for('verify_otp'))

@app.route('/verify-login-otp', methods=['GET', 'POST'])
def verify_login_otp():
    login_pending = session.get('login_pending')
    if not login_pending:
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_otp = request.form.get('otp', '').strip()
        if entered_otp != login_pending.get('otp'):
            flash('❌ Invalid OTP code!', 'error')
            return render_template('verify_login_otp.html', email=login_pending.get('email', ''))

        user = login_pending.get('user')
        session.clear()
        session['user_id'] = user['user_id']
        session['name'] = user['name']
        session['role'] = user['role']
        session['college_id'] = user.get('college_id') or 'kmbb1234'
        session['college_name'] = user.get('college_name') or 'KMBB College of Engineering and Technology'
        session['branch'] = user.get('branch', 'CSE')
        session['year'] = user.get('year', '1st Year')
        session['designation'] = user.get('designation', '')

        flash(f"Welcome back, {user['name']}!", 'success')
        if user['role'] == 'student':
            return redirect(url_for('student_dashboard'))
        elif user['role'] == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        return redirect(url_for('admin_dashboard'))

    return render_template('verify_login_otp.html', email=login_pending.get('email', ''))

@app.route('/register-college', methods=['POST'])
def register_college():
    c_name = request.form.get('college_name', '').strip()
    c_id = request.form.get('college_id', '').strip().lower()
    admin_id = request.form.get('admin_id', '').strip()
    admin_name = request.form.get('admin_name', '').strip()
    admin_email = request.form.get('admin_email', '').strip().lower()
    admin_password = request.form.get('admin_password', '').strip()
    entered_otp = request.form.get('email_otp', '').strip()

    stored_otp = session.get('onboard_otp')
    stored_email = session.get('onboard_email')

    if not stored_otp or entered_otp != stored_otp or admin_email != stored_email:
        flash('❌ Invalid or Missing Email OTP!', 'error')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM colleges WHERE college_id = %s", (c_id,))
    if cursor.fetchone():
        flash(f'⚠ College ID ({c_id}) is already registered!', 'error')
        cursor.close()
        return redirect(url_for('login'))

    cursor.execute("INSERT INTO colleges (college_id, college_name) VALUES (%s, %s)", (c_id, c_name))
    cursor.execute("""
        INSERT INTO users (user_id, name, email, role, password, status, college_id)
        VALUES (%s, %s, %s, 'admin', %s, 'approved', %s)
    """, (admin_id, admin_name, admin_email, admin_password, c_id))
    mysql.connection.commit()
    cursor.close()

    session.pop('onboard_otp', None)
    session.pop('onboard_email', None)

    flash(f'🎉 {c_name} successfully verified & registered!', 'success')
    return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        role = request.form.get('role')
        user_id = request.form.get('userId', '').strip()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s AND role = %s", (user_id, role))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            flash('No account found with this Role and User ID!', 'error')
            return render_template('forgot_password.html')

        otp = str(random.randint(100000, 999999))
        session['reset_data'] = {
            'user_id': user['user_id'],
            'email': user['email'],
            'name': user['name'],
            'otp': otp
        }

        sent = send_otp_email(user['email'], user['name'], otp, "Password Reset")
        if sent:
            flash(f"Reset code sent to registered email!", 'success')
            return redirect(url_for('verify_reset_otp'))
        else:
            flash("Could not send email. Please try again later.", 'error')
            return render_template('forgot_password.html')

    return render_template('forgot_password.html')

@app.route('/verify-reset-otp', methods=['GET', 'POST'])
def verify_reset_otp():
    reset_data = session.get('reset_data')
    if not reset_data:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        entered_otp = request.form.get('otp', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if entered_otp != reset_data['otp'] or new_password != confirm_password:
            flash('Invalid OTP or Passwords do not match!', 'error')
            return render_template('reset_password.html')

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (new_password, reset_data['user_id']))
        mysql.connection.commit()
        cursor.close()

        session.pop('reset_data', None)
        flash('Password updated successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')


@app.context_processor
def inject_user():
    if 'user_id' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        return dict(current_user=user)
    return dict(current_user=None)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    old_password = request.form.get('old_password', '')
    new_password = request.form.get('new_password', '')
    confirm_new_password = request.form.get('confirm_new_password', '')
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        flash('User not found!', 'error')
        return redirect(request.referrer or url_for('login'))
        
    if user['password'] != old_password:
        cursor.close()
        flash('❌ Incorrect Current Password. Changes not saved.', 'error')
        return redirect(request.referrer)
        
    update_pwd = user['password']
    if new_password:
        if new_password != confirm_new_password:
            cursor.close()
            flash('❌ New Passwords do not match!', 'error')
            return redirect(request.referrer)
        update_pwd = new_password
        
    cursor.execute('UPDATE users SET name = %s, email = %s, phone = %s, password = %s WHERE user_id = %s', (name, email, phone, update_pwd, session['user_id']))
    
    mysql.connection.commit()
    cursor.close()
    
    session['name'] = name
    flash('✅ Profile & Settings updated successfully!', 'success')
    return redirect(request.referrer)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# =========================================================
# LIBRARIAN DASHBOARD & OPERATIONS
# =========================================================
@app.route('/librarian-dashboard')
def librarian_dashboard():
    if session.get('role') != 'teacher' or session.get('designation') != 'Library Staff / Librarian':
        return redirect(url_for('login'))

    college_id = session.get('college_id', 'kmbb1234')
    user_id = session.get('user_id')
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM books WHERE college_id = %s ORDER BY book_name ASC", (college_id,))
    books = cursor.fetchall()

    cursor.execute("""
        SELECT bi.*, u.name as student_name, u.branch, u.year, b.book_name, b.author 
        FROM book_issues bi 
        JOIN users u ON bi.student_id = u.user_id 
        JOIN books b ON bi.book_code = b.book_code 
        WHERE bi.college_id = %s 
        ORDER BY bi.status ASC, bi.due_date ASC
    """, (college_id,))
    issued_books = cursor.fetchall()

    cursor.execute("SELECT user_id, name, branch, year FROM users WHERE role = 'student' AND (college_id = %s OR college_id IS NULL) ORDER BY name ASC", (college_id,))
    students = cursor.fetchall()

    cursor.execute("""
        SELECT user_id, name, designation, role 
        FROM users 
        WHERE (college_id = %s OR college_id IS NULL) 
          AND role IN ('admin', 'teacher') 
          AND role != 'student'
          AND (status = 'approved' OR status IS NULL) 
        ORDER BY role ASC, name ASC
    """, (college_id,))
    authorities = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM notices 
        WHERE recipient_id IS NULL OR recipient_id = %s OR sender_id = %s 
        ORDER BY created_at DESC LIMIT 15
    """, (user_id, user_id))
    notices = cursor.fetchall()

    cursor.close()
    return render_template('librarian-dashboard.html', 
                           name=session.get('name'),
                           college_name=session.get('college_name', 'KMBB College of Engineering and Technology'),
                           college_id=college_id,
                           books=books,
                           issued_books=issued_books,
                           students=students,
                           authorities=authorities,
                           notices=notices)

@app.route('/librarian/add-book', methods=['POST'])
def add_book():
    if session.get('role') != 'teacher' or session.get('designation') != 'Library Staff / Librarian':
        return redirect(url_for('login'))

    college_id = session.get('college_id', 'kmbb1234')
    book_code = request.form.get('book_code', '').strip()
    book_name = request.form.get('book_name', '').strip()
    author = request.form.get('author', '').strip()
    try:
        copies = int(request.form.get('total_copies', 5) or 5)
    except (ValueError, TypeError):
        copies = 5

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO books (college_id, book_code, book_name, author, total_copies, available_copies) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            total_copies = total_copies + VALUES(total_copies), 
            available_copies = available_copies + VALUES(available_copies)
    """, (college_id, book_code, book_name, author, copies, copies))
    mysql.connection.commit()
    cursor.close()

    flash(f'📚 Book "{book_name}" added successfully!', 'success')
    return redirect(url_for('librarian_dashboard'))

@app.route('/librarian/issue-book', methods=['POST'])
def issue_book():
    if session.get('role') != 'teacher' or session.get('designation') != 'Library Staff / Librarian':
        return redirect(url_for('login'))

    college_id = session.get('college_id', 'kmbb1234')
    student_id = request.form.get('student_id')
    book_code = request.form.get('book_code')
    try:
        days = int(request.form.get('duration_days', 14) or 14)
    except (ValueError, TypeError):
        days = 14

    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=days)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT available_copies, book_name FROM books WHERE book_code = %s AND college_id = %s", (book_code, college_id))
    book = cursor.fetchone()

    if not book or book['available_copies'] <= 0:
        cursor.close()
        flash('❌ Book is out of stock!', 'error')
        return redirect(url_for('librarian_dashboard'))

    cursor.execute("""
        INSERT INTO book_issues (college_id, student_id, book_code, borrow_date, due_date, status) 
        VALUES (%s, %s, %s, %s, %s, 'issued')
    """, (college_id, student_id, book_code, borrow_date, due_date))

    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_code = %s", (book_code,))

    notice_title = f"Library Book Issued: {book['book_name']}"
    notice_desc = f"You have been issued '{book['book_name']}'. Return due date: {due_date}."
    cursor.execute("""
        INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
        VALUES (%s, 'Library Notice', %s, 'College Librarian', %s, %s, 'teacher')
    """, (notice_title, notice_desc, student_id, session.get('user_id')))

    mysql.connection.commit()
    cursor.close()

    flash(f'✅ Book issued successfully to {student_id}!', 'success')
    return redirect(url_for('librarian_dashboard'))

@app.route('/librarian/approve-request/<int:issue_id>')
def approve_book_request(issue_id):
    if session.get('role') != 'teacher' or session.get('designation') != 'Library Staff / Librarian':
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT bi.*, b.book_name, b.available_copies 
        FROM book_issues bi 
        JOIN books b ON bi.book_code = b.book_code 
        WHERE bi.id = %s
    """, (issue_id,))
    issue = cursor.fetchone()

    if issue and issue['status'] == 'pending':
        if issue['available_copies'] <= 0:
            cursor.close()
            flash('❌ Out of stock!', 'error')
            return redirect(url_for('librarian_dashboard'))

        cursor.execute("UPDATE book_issues SET status = 'issued' WHERE id = %s", (issue_id,))
        cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_code = %s", (issue['book_code'],))
        mysql.connection.commit()
        flash(f'✅ Book request approved for {issue["student_id"]}!', 'success')

    cursor.close()
    return redirect(url_for('librarian_dashboard'))

@app.route('/librarian/return-book/<int:issue_id>')
def return_book(issue_id):
    if session.get('role') != 'teacher' or session.get('designation') != 'Library Staff / Librarian':
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM book_issues WHERE id = %s", (issue_id,))
    issue = cursor.fetchone()

    if issue and issue['status'] in ['issued', 'overdue']:
        cursor.execute("UPDATE book_issues SET status = 'returned' WHERE id = %s", (issue_id,))
        cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_code = %s", (issue['book_code'],))
        mysql.connection.commit()
        flash('✅ Book successfully marked as returned!', 'success')

    cursor.close()
    return redirect(url_for('librarian_dashboard'))

@app.route('/librarian/send-warning/<int:issue_id>')
def send_library_warning(issue_id):
    if session.get('role') != 'teacher' or session.get('designation') != 'Library Staff / Librarian':
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT bi.*, b.book_name, u.name as student_name 
        FROM book_issues bi 
        JOIN books b ON bi.book_code = b.book_code 
        JOIN users u ON bi.student_id = u.user_id 
        WHERE bi.id = %s
    """, (issue_id,))
    issue = cursor.fetchone()

    if issue:
        notice_title = f"⚠️ URGENT: Library Return Limit Overdue Notice!"
        notice_desc = f"Dear {issue['student_name']}, your return due date for '{issue['book_name']}' expired on {issue['due_date']}. Please return it immediately."
        cursor.execute("""
            INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
            VALUES (%s, 'Library Warning Notice', %s, 'Central Library Cell', %s, %s, 'teacher')
        """, (notice_title, notice_desc, issue['student_id'], session.get('user_id')))
        mysql.connection.commit()
        flash(f'🚨 Overdue notice sent to {issue["student_name"]}!', 'success')

    cursor.close()
    return redirect(url_for('librarian_dashboard'))

@app.route('/librarian/delete-issue/<int:issue_id>')
def delete_book_issue(issue_id):
    if session.get('role') != 'teacher' or session.get('designation') != 'Library Staff / Librarian':
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM book_issues WHERE id = %s", (issue_id,))
    issue = cursor.fetchone()

    if issue:
        if issue['status'] == 'issued':
            cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_code = %s", (issue['book_code'],))
        cursor.execute("DELETE FROM book_issues WHERE id = %s", (issue_id,))
        mysql.connection.commit()
        flash('🗑️ Book issue record deleted successfully!', 'success')

    cursor.close()
    return redirect(url_for('librarian_dashboard'))

@app.route('/student/request-book', methods=['POST'])
def student_request_book():
    if session.get('role') != 'student':
        return redirect(url_for('login'))

    student_id = session['user_id']
    college_id = session.get('college_id', 'kmbb1234')
    book_code = request.form.get('book_code')
    try:
        days = int(request.form.get('duration_days', 14) or 14)
    except (ValueError, TypeError):
        days = 14

    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=days)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM books WHERE book_code = %s AND college_id = %s", (book_code, college_id))
    book = cursor.fetchone()

    if not book or book['available_copies'] <= 0:
        cursor.close()
        flash('❌ Book is unavailable or out of stock!', 'error')
        return redirect(url_for('student_dashboard'))

    cursor.execute("""
        INSERT INTO book_issues (college_id, student_id, book_code, borrow_date, due_date, status) 
        VALUES (%s, %s, %s, %s, %s, 'pending')
    """, (college_id, student_id, book_code, borrow_date, due_date))

    mysql.connection.commit()
    cursor.close()

    flash(f'📖 Borrow request for "{book["book_name"]}" submitted! Librarian approval pending.', 'success')
    return redirect(url_for('student_dashboard'))

# =========================================================
# STUDENT DASHBOARD ROUTE
# =========================================================
@app.route('/student-dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    
    student_id = session['user_id']
    college_id = session.get('college_id', 'kmbb1234')
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (student_id,))
    student_profile = cursor.fetchone()

    branch = student_profile.get('branch') or 'CSE'
    year = student_profile.get('year') or '1st Year'

    current_subjects = SYLLABUS.get(branch, {}).get(year, COMMON_FIRST_YEAR)
    timetable_routine = get_or_create_timetable(cursor, branch, year)

    cursor.execute("SELECT * FROM books WHERE college_id = %s ORDER BY book_name ASC", (college_id,))
    available_books = cursor.fetchall()

    cursor.execute("""
        SELECT bi.*, b.book_name, b.author 
        FROM book_issues bi 
        JOIN books b ON bi.book_code = b.book_code 
        WHERE bi.student_id = %s 
        ORDER BY bi.due_date DESC
    """, (student_id,))
    my_books = cursor.fetchall()

    cursor.execute("SELECT * FROM student_fees WHERE student_id = %s ORDER BY id DESC", (student_id,))
    my_fees = cursor.fetchall()

    cursor.execute("SELECT * FROM fee_transactions WHERE student_id = %s ORDER BY created_at DESC", (student_id,))
    my_transactions = cursor.fetchall()

    cursor.execute("SELECT * FROM exam_marks WHERE student_id = %s ORDER BY created_at DESC", (student_id,))
    my_exam_marks = cursor.fetchall()

    cursor.execute("""
        SELECT r.*, u.name as staff_name, u.designation as staff_desig 
        FROM requests r 
        LEFT JOIN users u ON r.assigned_to = u.user_id 
        WHERE r.student_id = %s AND (r.student_hidden = FALSE OR r.student_hidden IS NULL)
        ORDER BY r.created_at DESC
    """, (student_id,))
    my_requests = cursor.fetchall()

    cursor.execute("SELECT * FROM complaints WHERE student_id = %s ORDER BY created_at DESC", (student_id,))
    my_complaints = cursor.fetchall()

    cursor.execute("SELECT * FROM document_requests WHERE student_id = %s ORDER BY created_at DESC", (student_id,))
    my_docs = cursor.fetchall()

    cursor.execute("SELECT * FROM mess_feedback WHERE student_id = %s ORDER BY created_at DESC", (student_id,))
    my_feedbacks = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM notices 
        WHERE recipient_id IS NULL OR recipient_id = %s 
        ORDER BY created_at DESC LIMIT 15
    """, (student_id,))
    notices = cursor.fetchall()

    cursor.execute("SELECT user_id, name, designation, branch FROM users WHERE role = 'teacher' AND designation != 'Hostel Warden' AND (status = 'approved' OR status IS NULL) ORDER BY name ASC")
    teachers = cursor.fetchall()

    cursor.execute("SELECT user_id, name, designation FROM users WHERE role = 'teacher' AND designation = 'Hostel Warden' AND (status = 'approved' OR status IS NULL) ORDER BY name ASC")
    wardens = cursor.fetchall()

    cursor.execute("SELECT user_id, name, designation, role, branch FROM users WHERE role IN ('admin', 'teacher') AND (status = 'approved' OR status IS NULL) ORDER BY role ASC, name ASC")
    authorities = cursor.fetchall()

    cursor.execute("SELECT * FROM notices WHERE category = 'Urgent Class Alert' ORDER BY created_at DESC LIMIT 1")
    urgent_alert = cursor.fetchone()

    today_name = datetime.now().strftime('%A')
    selected_day = request.args.get('day', today_name)
    if selected_day not in DAYS_LIST:
        selected_day = today_name

    cursor.execute("SELECT * FROM mess_menu WHERE day_name = %s", (selected_day,))
    mess_menu = cursor.fetchone()

    subject_attendance = []
    total_all_classes = 0
    total_all_present = 0

    for sub in current_subjects:
        cursor.execute("SELECT COUNT(*) AS total FROM attendance WHERE student_id = %s AND subject = %s", (student_id, sub))
        sub_total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) AS present FROM attendance WHERE student_id = %s AND subject = %s AND status = 'Present'", (student_id, sub))
        sub_present = cursor.fetchone()['present']
        sub_pct = round((sub_present / sub_total * 100), 1) if sub_total > 0 else 100.0

        subject_attendance.append({
            'name': sub,
            'total': sub_total,
            'present': sub_present,
            'absent': (sub_total - sub_present),
            'percentage': sub_pct,
            'is_low': (sub_pct < 75.0)
        })
        total_all_classes += sub_total
        total_all_present += sub_present

    overall_pct = round((total_all_present / total_all_classes * 100), 1) if total_all_classes > 0 else 100.0

    week_start = date.today() - timedelta(days=7)
    cursor.execute("SELECT COUNT(*) AS total FROM attendance WHERE student_id = %s AND date >= %s", (student_id, week_start))
    week_total = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) AS present FROM attendance WHERE student_id = %s AND status = 'Present' AND date >= %s", (student_id, week_start))
    week_present = cursor.fetchone()['present']
    week_pct = round((week_present / week_total * 100), 1) if week_total > 0 else 100.0

    month_start = date.today() - timedelta(days=30)
    cursor.execute("SELECT COUNT(*) AS total FROM attendance WHERE student_id = %s AND date >= %s", (student_id, month_start))
    month_total = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) AS present FROM attendance WHERE student_id = %s AND status = 'Present' AND date >= %s", (student_id, month_start))
    month_present = cursor.fetchone()['present']
    month_pct = round((month_present / month_total * 100), 1) if month_total > 0 else 100.0

    attendance_stats = {
        'overall_pct': overall_pct,
        'total_classes': total_all_classes,
        'total_present': total_all_present,
        'is_low': (overall_pct < 75.0),
        'week_total': week_total,
        'week_present': week_present,
        'week_pct': week_pct,
        'month_total': month_total,
        'month_present': month_present,
        'month_pct': month_pct,
        'subjects': subject_attendance
    }

    cursor.execute("""
        SELECT * FROM hostel_allocations 
        WHERE student_id = %s 
        ORDER BY id DESC LIMIT 1
    """, (student_id,))
    my_hostel = cursor.fetchone()

    cursor.execute("SELECT * FROM student_placements WHERE student_id = %s ORDER BY date_added DESC", (student_id,))
    my_placements = cursor.fetchall()
    
    cursor.close()

    return render_template('student-dashboard.html', 
                           name=session.get('name'), 
                           student_id=student_id,
                           student_profile=student_profile,
                           college_name=session.get('college_name', 'KMBB College of Engineering and Technology'),
                           college_id=college_id,
                           branch=branch,
                           year=year,
                           available_books=available_books,
                           my_books=my_books,
                           my_fees=my_fees,
                           my_transactions=my_transactions,
                           my_hostel=my_hostel,
                           requests=my_requests, 
                           complaints=my_complaints, 
                           doc_requests=my_docs,
                           my_feedbacks=my_feedbacks,
                           my_exam_marks=my_exam_marks,
                           my_placements=my_placements,
                           notices=notices,
                           teachers=teachers,
                           wardens=wardens,
                           authorities=authorities,
                           urgent_alert=urgent_alert,
                           mess_menu=mess_menu,
                           timetable_routine=timetable_routine,
                           days_list=DAYS_LIST,
                           selected_day=selected_day,
                           today_name=today_name,
                           att=attendance_stats)

@app.route('/student/pay-fee', methods=['POST'])
def student_pay_fee():
    if session.get('role') != 'student':
        return redirect(url_for('login'))

    student_id = session['user_id']
    college_id = session.get('college_id', 'kmbb1234')
    semester = request.form.get('semester')
    try:
        amount = float(request.form.get('amount', 0))
    except (ValueError, TypeError):
        flash('❌ Invalid payment amount! Please enter a valid number.', 'error')
        return redirect(url_for('student_dashboard'))
    payment_mode = request.form.get('payment_mode', 'UPI')
    transaction_ref_no = request.form.get('transaction_ref_no', '').strip()
    payment_date = request.form.get('payment_date', date.today().strftime('%Y-%m-%d'))
    remarks = request.form.get('remarks', 'Semester Fee Payment').strip()

    if not transaction_ref_no or amount <= 0:
        flash('❌ Invalid transaction details!', 'error')
        return redirect(url_for('student_dashboard'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO fee_transactions (college_id, student_id, amount, payment_mode, transaction_ref_no, payment_date, remarks, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending_verification')
    """, (college_id, student_id, amount, payment_mode, transaction_ref_no, payment_date, remarks))

    cursor.execute("SELECT user_id FROM users WHERE designation = 'Accountant / Clerk' AND college_id = %s LIMIT 1", (college_id,))
    accountant = cursor.fetchone()
    accountant_id = accountant['user_id'] if accountant else None

    notice_title = f"New Fee Payment: ₹{amount} from {student_id}"
    notice_desc = f"Student {session.get('name')} (Roll: {student_id}) submitted ₹{amount} via {payment_mode} (Ref: {transaction_ref_no})."

    cursor.execute("""
        INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
        VALUES (%s, 'Fee Alert', %s, %s, %s, %s, 'student')
    """, (notice_title, notice_desc, session.get('name'), accountant_id, student_id))

    # ---------------------------------------------------------
    # AUTOMATED EMAIL ALERTS (Flask-Mail)
    # ---------------------------------------------------------
    if accountant_id:
        cursor.execute("SELECT email FROM users WHERE user_id = %s", (accountant_id,))
        acc_record = cursor.fetchone()
        if acc_record and acc_record.get('email'):
            try:
                msg = Message(f"Fee Payment Alert: {student_id}", recipients=[acc_record['email']])
                msg.body = notice_desc
                mail.send(msg)
            except Exception:
                pass
    # ---------------------------------------------------------

    mysql.connection.commit()
    cursor.close()

    flash(f'✅ Payment slip submitted to Accounts!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/delete-student-fee/<int:fee_id>')
def delete_student_fee(fee_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    user_role = session.get('role')
    user_desig = session.get('designation', '')

    cursor = mysql.connection.cursor()
    if user_role == 'admin' or user_desig == 'Accountant / Clerk':
        cursor.execute("DELETE FROM student_fees WHERE id = %s", (fee_id,))
    elif user_role == 'student':
        cursor.execute("DELETE FROM student_fees WHERE id = %s AND student_id = %s", (fee_id, user_id))

    mysql.connection.commit()
    cursor.close()

    flash('🗑️ Fee structure record deleted successfully!', 'success')
    if user_desig == 'Accountant / Clerk':
        return redirect(url_for('accountant_dashboard'))
    return redirect(url_for('student_dashboard'))

@app.route('/delete-fee-transaction/<int:tx_id>')
def delete_fee_transaction(tx_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    user_role = session.get('role')
    user_desig = session.get('designation', '')

    cursor = mysql.connection.cursor()
    if user_role == 'admin' or user_desig == 'Accountant / Clerk':
        cursor.execute("DELETE FROM fee_transactions WHERE id = %s", (tx_id,))
    elif user_role == 'student':
        cursor.execute("DELETE FROM fee_transactions WHERE id = %s AND student_id = %s", (tx_id, user_id))

    mysql.connection.commit()
    cursor.close()

    flash('🗑️ Fee payment slip record deleted successfully!', 'success')
    if user_desig == 'Accountant / Clerk':
        return redirect(url_for('accountant_dashboard'))
    return redirect(url_for('student_dashboard'))

@app.route('/accountant-dashboard')
def accountant_dashboard():
    if session.get('role') != 'teacher' or session.get('designation') != 'Accountant / Clerk':
        flash('❌ Access Denied: Only Accounts Department can access this portal!', 'error')
        return redirect(url_for('login'))

    college_id = session.get('college_id', 'kmbb1234')
    user_id = session.get('user_id')
    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT ft.*, u.name as student_name, u.branch, u.year
        FROM fee_transactions ft
        JOIN users u ON ft.student_id = u.user_id
        WHERE ft.college_id = %s
        ORDER BY ft.status ASC, ft.created_at DESC
    """, (college_id,))
    transactions = cursor.fetchall()

    cursor.execute("""
        SELECT sf.*, u.name as student_name, u.branch, u.year
        FROM student_fees sf
        JOIN users u ON sf.student_id = u.user_id
        WHERE sf.college_id = %s
        ORDER BY sf.due_date ASC
    """, (college_id,))
    student_fees = cursor.fetchall()

    cursor.execute("SELECT COALESCE(SUM(paid_fee), 0) AS total_collected FROM student_fees WHERE college_id = %s", (college_id,))
    total_collected = cursor.fetchone()['total_collected']

    cursor.execute("SELECT COALESCE(SUM(due_fee), 0) AS total_dues FROM student_fees WHERE college_id = %s", (college_id,))
    total_dues = cursor.fetchone()['total_dues']

    cursor.execute("SELECT COUNT(*) AS unverified_count FROM fee_transactions WHERE college_id = %s AND status = 'pending_verification'", (college_id,))
    unverified_count = cursor.fetchone()['unverified_count']

    cursor.execute("SELECT user_id, name, branch, year FROM users WHERE role = 'student' AND (college_id = %s OR college_id IS NULL) ORDER BY name ASC", (college_id,))
    students = cursor.fetchall()

    cursor.execute("""
        SELECT user_id, name, designation, role 
        FROM users 
        WHERE (college_id = %s OR college_id IS NULL) 
          AND role IN ('admin', 'teacher') 
          AND role != 'student'
          AND (status = 'approved' OR status IS NULL) 
        ORDER BY role ASC, name ASC
    """, (college_id,))
    authorities = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM notices 
        WHERE recipient_id IS NULL OR recipient_id = %s OR sender_id = %s 
        ORDER BY created_at DESC LIMIT 15
    """, (user_id, user_id))
    notices = cursor.fetchall()

    cursor.close()

    stats = {
        'total_collected': total_collected,
        'total_dues': total_dues,
        'unverified_count': unverified_count,
        'total_records': len(student_fees)
    }

    return render_template('accountant-dashboard.html',
                           name=session.get('name'),
                           college_name=session.get('college_name', 'KMBB College of Engineering and Technology'),
                           college_id=college_id,
                           transactions=transactions,
                           student_fees=student_fees,
                           students=students,
                           authorities=authorities,
                           notices=notices,
                           stats=stats)

@app.route('/accountant/verify-payment/<int:tx_id>/<string:status>')
def verify_payment(tx_id, status):
    if session.get('role') != 'teacher' or session.get('designation') != 'Accountant / Clerk':
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM fee_transactions WHERE id = %s", (tx_id,))
    tx = cursor.fetchone()

    if tx and tx['status'] == 'pending_verification':
        accountant_name = session.get('name', 'Accountant')

        if status == 'verified':
            cursor.execute("UPDATE fee_transactions SET status = 'verified', verified_by = %s WHERE id = %s", (accountant_name, tx_id))
            
            cursor.execute("SELECT * FROM student_fees WHERE student_id = %s ORDER BY id DESC LIMIT 1", (tx['student_id'],))
            fee_record = cursor.fetchone()
            if fee_record:
                new_paid = float(fee_record['paid_fee']) + float(tx['amount'])
                new_due = max(0.0, float(fee_record['total_fee']) - new_paid)
                new_status = 'paid' if new_due == 0 else 'partial'
                cursor.execute("""
                    UPDATE student_fees SET paid_fee = %s, due_fee = %s, status = %s WHERE id = %s
                """, (new_paid, new_due, new_status, fee_record['id']))

            notice_title = f"Fee Payment Verified: ₹{tx['amount']}"
            notice_desc = f"Your fee payment of ₹{tx['amount']} (Ref: {tx['transaction_ref_no']}) has been VERIFIED & APPROVED by Accounts Department."
            cursor.execute("""
                INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
                VALUES (%s, 'Fee Notice', %s, 'Accounts Department', %s, %s, 'teacher')
            """, (notice_title, notice_desc, tx['student_id'], session.get('user_id')))

            flash(f'✅ Transaction Ref {tx["transaction_ref_no"]} verified! Student dues updated.', 'success')

        elif status == 'rejected':
            cursor.execute("UPDATE fee_transactions SET status = 'rejected', verified_by = %s WHERE id = %s", (accountant_name, tx_id))
            notice_title = f"Fee Payment Rejected: Ref {tx['transaction_ref_no']}"
            notice_desc = f"Your submitted payment reference {tx['transaction_ref_no']} was REJECTED by Accounts."
            cursor.execute("""
                INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
                VALUES (%s, 'Fee Notice', %s, 'Accounts Department', %s, %s, 'teacher')
            """, (notice_title, notice_desc, tx['student_id'], session.get('user_id')))

            flash(f'❌ Payment reference {tx["transaction_ref_no"]} rejected.', 'error')

        mysql.connection.commit()

    cursor.close()
    return redirect(url_for('accountant_dashboard'))

@app.route('/accountant/assign-fee', methods=['POST'])
def assign_fee_structure():
    if session.get('role') != 'teacher' or session.get('designation') != 'Accountant / Clerk':
        return redirect(url_for('login'))

    college_id = session.get('college_id', 'kmbb1234')
    student_id = request.form.get('student_id')
    semester = request.form.get('semester')
    try:
        total_fee = float(request.form.get('total_fee', 50000.00) or 50000.00)
        paid_fee = float(request.form.get('paid_fee', 0.00) or 0.00)
    except (ValueError, TypeError):
        flash('❌ Invalid numeric amount entered for fee structure!', 'danger')
        return redirect(url_for('accountant_dashboard'))

    due_date = request.form.get('due_date', (date.today() + timedelta(days=30)).strftime('%Y-%m-%d'))

    due_fee = max(0.0, total_fee - paid_fee)
    status = 'paid' if due_fee == 0 else ('partial' if paid_fee > 0 else 'pending')

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO student_fees (college_id, student_id, semester, total_fee, paid_fee, due_fee, due_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (college_id, student_id, semester, total_fee, paid_fee, due_fee, due_date, status))

    notice_title = f"New Fee Dues Allocated: {semester}"
    notice_desc = f"Semester fee structure for {semester} updated. Total: ₹{total_fee}, Dues: ₹{due_fee}, Return Due Date: {due_date}."
    cursor.execute("""
        INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
        VALUES (%s, 'Fee Notice', %s, 'Accounts Department', %s, %s, 'teacher')
    """, (notice_title, notice_desc, student_id, session.get('user_id')))

    mysql.connection.commit()
    cursor.close()

    flash(f'✅ Fee structure assigned successfully to student {student_id}!', 'success')
    return redirect(url_for('accountant_dashboard'))

@app.route('/accountant/send-fee-warning/<int:fee_id>')
def send_fee_warning(fee_id):
    if session.get('role') != 'teacher' or session.get('designation') != 'Accountant / Clerk':
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT sf.*, u.name as student_name
        FROM student_fees sf
        JOIN users u ON sf.student_id = u.user_id
        WHERE sf.id = %s
    """, (fee_id,))
    fee = cursor.fetchone()

    if fee:
        notice_title = f"⚠️ URGENT: College Semester Fee Dues Reminder!"
        notice_desc = f"Dear {fee['student_name']}, your pending fee dues of ₹{fee['due_fee']} for {fee['semester']} were due on {fee['due_date']}. Please clear immediately."
        cursor.execute("""
            INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
            VALUES (%s, 'Fee Notice', %s, 'Accounts Office', %s, %s, 'teacher')
        """, (notice_title, notice_desc, fee['student_id'], session.get('user_id')))
        mysql.connection.commit()
        flash(f'🚨 Fee payment reminder notice dispatched to {fee["student_name"]}!', 'success')

    cursor.close()
    return redirect(url_for('accountant_dashboard'))

@app.route('/apply-request', methods=['POST'])
def apply_request():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    req_type = request.form.get('type')
    reason = request.form.get('reason')
    assigned_to = request.form.get('assigned_to')
    student_id = session['user_id']
    if req_type and reason and assigned_to:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO requests (student_id, assigned_to, type, reason) VALUES (%s, %s, %s, %s)", (student_id, assigned_to, req_type, reason))
        mysql.connection.commit()
        cursor.close()
        flash(f'✅ Request sent successfully!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/apply-document', methods=['POST'])
def apply_document():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    doc_type = request.form.get('doc_type', '').strip()
    purpose = request.form.get('purpose', '').strip()
    student_id = session['user_id']
    if doc_type and purpose:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO document_requests (student_id, doc_type, purpose, status) VALUES (%s, %s, %s, 'Pending HOD')", (student_id, doc_type, purpose))
        mysql.connection.commit()
        cursor.close()
        flash('✅ Certificate request submitted!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    title = request.form.get('title')
    description = request.form.get('description')
    student_id = session['user_id']
    if title and description:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO complaints (student_id, title, description, status) VALUES (%s, %s, %s, 'pending')", (student_id, title, description))
        
        cursor.execute("SELECT user_id FROM users WHERE role = 'admin' LIMIT 1")
        admin = cursor.fetchone()
        if admin:
            cursor.execute("""
                INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
                VALUES (%s, 'Repair / Maintenance Complaint', %s, %s, %s, %s, 'student')
            """, (f"New Repair Complaint: {title}", f"Student {session.get('name')} (Roll: {student_id}) filed a repair/electrical complaint: {description}", session.get('name'), admin['user_id'], student_id))

        mysql.connection.commit()
        cursor.close()
        flash('⚡ Repair/Electrical complaint filed successfully and sent to Admin!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/admin/forward-complaint/<int:comp_id>', methods=['POST'])
def forward_complaint_to_electrician(comp_id):
    if session.get('role') not in ['admin', 'teacher']:
        return redirect(url_for('login'))

    electrician_id = request.form.get('electrician_id')
    forward_remarks = request.form.get('forward_remarks', 'Please inspect and repair immediately.').strip()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT c.*, u.name as student_name FROM complaints c JOIN users u ON c.student_id = u.user_id WHERE c.id = %s", (comp_id,))
    comp = cursor.fetchone()

    if comp:
        cursor.execute("UPDATE complaints SET status = 'forwarded_to_electrician' WHERE id = %s", (comp_id,))
        
        notice_title = f"⚡ Repair Task Assigned: {comp['title']}"
        notice_desc = f"Task forwarded by Admin. Student: {comp['student_name']} ({comp['student_id']}). Issue: {comp['description']}. Instructions: {forward_remarks}"
        cursor.execute("""
            INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
            VALUES (%s, 'Electrical / Repair Work Order', %s, %s, %s, %s, 'admin')
        """, (notice_title, notice_desc, session.get('name'), electrician_id, session.get('user_id')))

        cursor.execute("""
            INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
            VALUES (%s, 'Complaint Status Update', %s, 'Campus Administration', %s, %s, 'admin')
        """, (f"Complaint Forwarded: {comp['title']}", f"Your complaint has been forwarded to the campus electrician for repair work.", comp['student_id'], session.get('user_id')))

        mysql.connection.commit()
        flash('✅ Complaint successfully assigned to the electrician by Admin!', 'success')

    cursor.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/electrician/update-repair/<int:comp_id>', methods=['POST'])
def electrician_update_repair(comp_id):
    if session.get('role') != 'teacher' or session.get('designation') != 'Electrician':
        return redirect(url_for('login'))

    status = request.form.get('status', 'resolved')
    reply_remarks = request.form.get('reply_remarks', '').strip()
    electrician_name = session.get('name', 'Electrician')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT c.*, u.name as student_name FROM complaints c JOIN users u ON c.student_id = u.user_id WHERE c.id = %s", (comp_id,))
    comp = cursor.fetchone()

    if comp:
        cursor.execute("UPDATE complaints SET status = %s WHERE id = %s", (status, comp_id))

        stud_title = f"⚡ Repair Update: {comp['title']}"
        stud_desc = f"Electrician {electrician_name} updated status to '{status.replace('_', ' ').capitalize()}'. Remarks: {reply_remarks}"
        cursor.execute("""
            INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
            VALUES (%s, 'Repair Feedback', %s, %s, %s, %s, 'teacher')
        """, (stud_title, stud_desc, electrician_name, comp['student_id'], session.get('user_id')))

        cursor.execute("SELECT user_id FROM users WHERE role = 'admin' LIMIT 1")
        admin = cursor.fetchone()
        if admin:
            cursor.execute("""
                INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
                VALUES (%s, 'Repair Task Completed', %s, %s, %s, %s, 'teacher')
            """, (f"Electrician Report: {comp['title']}", f"Electrician {electrician_name} resolved complaint for student {comp['student_name']}. Reply: {reply_remarks}", electrician_name, admin['user_id'], session.get('user_id')))

        mysql.connection.commit()
        flash('✅ Repair status and reply updated successfully!', 'success')

    cursor.close()
    return redirect(url_for('teacher_dashboard'))

@app.route('/submit-mess-feedback', methods=['POST'])
def submit_mess_feedback():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    day_name = request.form.get('day_name', 'Today')
    meal_type = request.form.get('meal_type')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    student_id = session['user_id']
    if meal_type and rating:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO mess_feedback (student_id, day_name, meal_type, rating, comment) VALUES (%s, %s, %s, %s, %s)", (student_id, day_name, meal_type, rating, comment))
        mysql.connection.commit()
        cursor.close()
        flash('Mess feedback submitted!', 'success')
    return redirect(url_for('student_dashboard', day=day_name))

@app.route('/print-pass/<int:req_id>')
def print_pass(req_id):
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM requests WHERE id = %s AND student_id = %s", (req_id, session['user_id']))
    req = cursor.fetchone()
    cursor.close()
    if req and req['status'] == 'approved':
        # ---------------------------------------------------------
        # NEW FEATURE 6: QR-VERIFIED DIGITAL PASSES
        # ---------------------------------------------------------
        qr_data = f"CAMPUS_PASS_{session['user_id']}_REQ_{req_id}_VERIFIED"
        img = qrcode.make(qr_data)
        buffered = BytesIO()
        img.save(buffered)
        qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return render_template('print_pass.html', req=req, student_name=session.get('name'), qr_base64=qr_base64)
    flash('Pass is not approved yet for printing!', 'error')
    return redirect(url_for('student_dashboard'))

# =========================================================
# TEACHER / STAFF DASHBOARD ROUTE (WITH ALL STUDENTS FETCHED FOR MESSAGING)
# =========================================================
@app.route('/teacher-dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        flash('Please login as Faculty/Staff first!', 'error')
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    college_id = session.get('college_id', 'kmbb1234')
    selected_branch = request.args.get('branch', session.get('branch', 'CSE'))
    selected_year = request.args.get('year', session.get('year', '1st Year'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    staff_profile = cursor.fetchone() or {}

    cursor.execute("""
        SELECT r.*, u.name as student_name 
        FROM requests r 
        LEFT JOIN users u ON r.student_id = u.user_id 
        WHERE r.assigned_to = %s AND (r.teacher_hidden = FALSE OR r.teacher_hidden IS NULL)
        ORDER BY r.created_at DESC
    """, (user_id,))
    assigned_requests = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM notices 
        WHERE recipient_id IS NULL OR recipient_id = %s OR sender_id = %s 
        ORDER BY created_at DESC LIMIT 20
    """, (user_id, user_id))
    notices = cursor.fetchall()

    cursor.execute("""
        SELECT user_id, name, email, branch, year 
        FROM users 
        WHERE role = 'student' 
          AND branch = %s 
          AND year = %s 
          AND (status = 'approved' OR status IS NULL) 
        ORDER BY user_id
    """, (selected_branch, selected_year))
    students = cursor.fetchall()

    cursor.execute("""
        SELECT user_id, name, email, branch, year 
        FROM users 
        WHERE role = 'student' AND (status = 'approved' OR status IS NULL) 
        ORDER BY name ASC
    """)
    all_students = cursor.fetchall()

    cursor.execute("SELECT user_id, name FROM users WHERE designation = 'Electrician' AND (college_id = %s OR college_id IS NULL)", (college_id,))
    electricians = cursor.fetchall()

    staff_designation = staff_profile.get('designation', '')
    if staff_designation == 'Electrician':
        cursor.execute("""
            SELECT c.*, u.name as student_name, u.branch, u.year 
            FROM complaints c 
            JOIN users u ON c.student_id = u.user_id 
            WHERE c.status IN ('forwarded_to_electrician', 'in_progress', 'resolved')
            ORDER BY c.created_at DESC
        """)
    else:
        cursor.execute("""
            SELECT c.*, u.name as student_name, u.branch, u.year 
            FROM complaints c 
            JOIN users u ON c.student_id = u.user_id 
            ORDER BY c.created_at DESC
        """)
    all_complaints = cursor.fetchall()

    routine = get_or_create_timetable(cursor, selected_branch, selected_year)

    cursor.execute("""
        SELECT em.*, u.name as student_name, u.branch, u.year 
        FROM exam_marks em 
        LEFT JOIN users u ON em.student_id = u.user_id 
        ORDER BY em.created_at DESC LIMIT 50
    """)
    recent_marks = cursor.fetchall()

    # Authorities and Staff for messaging
    cursor.execute("""
        SELECT user_id, name, designation, role 
        FROM users 
        WHERE role IN ('admin', 'teacher') AND user_id != %s AND (status = 'approved' OR status IS NULL)
        ORDER BY name ASC
    """, (user_id,))
    authorities = cursor.fetchall()
    authorities = cursor.fetchall()

    # Document Requests for HOD and Principal
    doc_requests = []
    if staff_designation == 'Head of Department (HOD)':
        hod_branch = staff_profile.get('branch')
        cursor.execute("""
            SELECT d.*, u.name as student_name 
            FROM document_requests d 
            JOIN users u ON d.student_id = u.user_id 
            WHERE d.status = 'Pending HOD' AND u.branch = %s
            ORDER BY d.created_at DESC
        """, (hod_branch,))
        doc_requests = cursor.fetchall()
    elif staff_designation == 'Principal':
        cursor.execute("""
            SELECT d.*, u.name as student_name 
            FROM document_requests d 
            JOIN users u ON d.student_id = u.user_id 
            WHERE d.status = 'Pending Principal'
            ORDER BY d.created_at DESC
        """)
        doc_requests = cursor.fetchall()

    cursor.execute("""
        SELECT sp.*, u.name as student_name, u.branch, u.year 
        FROM student_placements sp
        JOIN users u ON sp.student_id = u.user_id
        WHERE u.college_id = %s
        ORDER BY sp.date_added DESC
    """, (college_id,))
    student_placements = cursor.fetchall()

    cursor.close()

    available_subjects = SYLLABUS.get(selected_branch, {}).get(selected_year, COMMON_FIRST_YEAR)

    return render_template('teacher-dashboard.html', 
                           name=session.get('name', 'Faculty Member'), 
                           student_placements=student_placements,
                           user_id=user_id,
                           profile=staff_profile,
                           college_name=session.get('college_name', 'KMBB College of Engineering and Technology'),
                           college_id=college_id,
                           is_principal=(staff_designation == 'Principal'),
                           is_teacher=(staff_designation in ['Teacher / Professor', 'Head of Department (HOD)']),
                           is_warden=(staff_designation == 'Hostel Warden'),
                           is_electrician=(staff_designation == 'Electrician'),
                           is_exam_cell=(staff_designation == 'Examination Cell / Controller'),
                           requests=assigned_requests, 
                           notices=notices,
                           students=students,
                           all_students=all_students,
                           electricians=electricians,
                           all_complaints=all_complaints,
                           doc_requests=doc_requests,
                           authorities=authorities,
                           recent_marks=recent_marks,
                           syllabus_dict=SYLLABUS,
                           branches=BRANCHES,
                           years=YEARS,
                           selected_branch=selected_branch,
                           selected_year=selected_year,
                           subjects=available_subjects,
                           routine=routine,
                           today_date=date.today().strftime('%Y-%m-%d'))

@app.route('/warden/allocate-room', methods=['POST'])
def warden_allocate_room():
    if session.get('role') != 'teacher' or session.get('designation') != 'Hostel Warden':
        return redirect(url_for('login'))

    student_id = request.form.get('student_id')
    hostel_name = request.form.get('hostel_name', '').strip()
    floor_no = request.form.get('floor_no', '').strip()
    room_no = request.form.get('room_no', '').strip()
    warden_name = session.get('name', 'Hostel Warden')
    college_id = session.get('college_id', 'kmbb1234')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name FROM users WHERE user_id = %s", (student_id,))
    stud = cursor.fetchone()
    stud_name = stud['name'] if stud else student_id

    # Record in hostel_allocations table
    cursor.execute("""
        INSERT INTO hostel_allocations (college_id, student_id, hostel_name, room_number, floor_number, status, allocated_by, allocated_by_id, allocated_at)
        VALUES (%s, %s, %s, %s, %s, 'allocated', %s, %s, NOW())
    """, (college_id, student_id, hostel_name, room_no, floor_no, warden_name, session.get('user_id')))

    notice_title = f"🏠 Hostel Room Allocated: {hostel_name}"
    notice_desc = f"Dear {stud_name}, your hostel room has been successfully allocated by Warden {warden_name}. Hostel: {hostel_name}, Floor: {floor_no}, Room No: {room_no}."
    
    cursor.execute("""
        INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
        VALUES (%s, 'Hostel Room Allocation', %s, %s, %s, %s, 'teacher')
    """, (notice_title, notice_desc, warden_name, student_id, session.get('user_id')))
    
    # ---------------------------------------------------------
    # NEW FEATURE 2: AUTOMATED EMAIL ALERTS (Flask-Mail)
    # ---------------------------------------------------------
    cursor.execute("SELECT email FROM users WHERE user_id = %s", (student_id,))
    stud_record = cursor.fetchone()
    if stud_record and stud_record.get('email'):
        try:
            msg = Message("Hostel Room Allocated", recipients=[stud_record['email']])
            msg.body = notice_desc
            mail.send(msg)
        except Exception:
            pass
    # ---------------------------------------------------------
    
    mysql.connection.commit()
    cursor.close()

    flash(f'✅ Room successfully allocated to student {student_id}!', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))
    branch = request.form.get('branch')
    year = request.form.get('year')
    subject = request.form.get('subject')
    att_date = request.form.get('date', date.today().strftime('%Y-%m-%d'))
    teacher_name = session.get('name')
    teacher_id = session.get('user_id')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_id, name FROM users WHERE role = 'student' AND branch = %s AND year = %s AND (status = 'approved' OR status IS NULL)", (branch, year))
    students = cursor.fetchall()

    for s in students:
        s_id = s['user_id']
        status = request.form.get(f'status_{s_id}', 'Present')
        cursor.execute("SELECT id FROM attendance WHERE student_id = %s AND subject = %s AND date = %s", (s_id, subject, att_date))
        exists = cursor.fetchone()
        if exists:
            cursor.execute("UPDATE attendance SET status = %s, marked_by = %s WHERE id = %s", (status, teacher_name, exists['id']))
        else:
            cursor.execute("INSERT INTO attendance (student_id, subject, date, status, marked_by) VALUES (%s, %s, %s, %s, %s)", (s_id, subject, att_date, status, teacher_name))

        cursor.execute("""
            INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
            VALUES (%s, 'Attendance Notification', %s, %s, %s, %s, 'teacher')
        """, (f"Attendance: {subject} ({status})", f"Attendance for '{subject}' on {att_date} marked as '{status}'.", f"{teacher_name} (Teacher)", s_id, teacher_id))

    mysql.connection.commit()
    cursor.close()
    flash('Attendance saved successfully!', 'success')
    return redirect(url_for('teacher_dashboard', branch=branch, year=year))

@app.route('/update-request/<int:req_id>/<string:status>')
def update_request(req_id, status):
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE requests SET status = %s WHERE id = %s AND assigned_to = %s", (status, req_id, session['user_id']))
    mysql.connection.commit()
    cursor.close()
    flash(f'Request marked as {status}!', 'success')
    return redirect(url_for('teacher_dashboard'))

# =========================================================
# ADMIN DASHBOARD ROUTE
# =========================================================
@app.route('/admin-dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Please login as College Admin first!', 'error')
        return redirect(url_for('login'))

    admin_id = session.get('user_id')
    college_id = session.get('college_id', 'kmbb1234')
    selected_branch = request.args.get('branch', 'CSE')
    selected_year = request.args.get('year', '1st Year')

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (admin_id,))
    current_admin = cursor.fetchone() or {'name': session.get('name'), 'email': 'admin@demo.com'}

    cursor.execute("SELECT * FROM colleges WHERE college_id = %s", (college_id,))
    current_college = cursor.fetchone()
    college_name = current_college['college_name'] if current_college else session.get('college_name', 'KMBB College of Engineering and Technology')

    cursor.execute("SELECT * FROM users WHERE designation = 'Principal' LIMIT 1")
    current_principal = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM users 
        WHERE role = 'teacher' AND (status = 'approved' OR status IS NULL) 
        ORDER BY user_id
    """)
    all_staff = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM users 
        WHERE role = 'student' AND (status = 'approved' OR status IS NULL) 
        ORDER BY user_id
    """)
    all_students = cursor.fetchall()

    cursor.execute("SELECT user_id, name FROM users WHERE designation = 'Electrician' AND (college_id = %s OR college_id IS NULL)", (college_id,))
    electricians = cursor.fetchall()

    cursor.execute("""
        SELECT c.*, u.name as student_name 
        FROM complaints c 
        LEFT JOIN users u ON c.student_id = u.user_id 
        ORDER BY c.created_at DESC
    """)
    raw_complaints = cursor.fetchall()
    complaints = []
    now = datetime.now()
    for c in raw_complaints:
        c_dict = dict(c)
        days_old = (now - c['created_at']).days if c.get('created_at') else 0
        c_dict['age_days'] = days_old
        c_dict['is_urgent'] = (days_old >= 2 and c.get('status') != 'resolved')
        complaints.append(c_dict)

    cursor.execute("""
        SELECT d.*, u.name as student_name 
        FROM document_requests d 
        LEFT JOIN users u ON d.student_id = u.user_id 
        ORDER BY d.created_at DESC
    """)
    doc_requests = cursor.fetchall()

    cursor.execute("""
        SELECT mf.*, u.name as student_name, u.branch, u.year 
        FROM mess_feedback mf 
        LEFT JOIN users u ON mf.student_id = u.user_id 
        ORDER BY mf.created_at DESC
    """)
    feedbacks = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM notices 
        WHERE recipient_id IS NULL OR recipient_id = %s OR sender_id = %s 
        ORDER BY created_at DESC LIMIT 25
    """, (admin_id, admin_id))
    notices = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS count FROM complaints WHERE status != 'resolved'")
    open_complaints = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) AS count FROM document_requests WHERE status = 'Pending Admin'")
    pending_docs = cursor.fetchone()['count']

    admin_routine = get_or_create_timetable(cursor, selected_branch, selected_year)
    
    cursor.execute("""
        SELECT sp.*, u.name as student_name, u.branch, u.year 
        FROM student_placements sp
        JOIN users u ON sp.student_id = u.user_id
        WHERE u.college_id = %s
        ORDER BY sp.date_added DESC
    """, (college_id,))
    student_placements = cursor.fetchall()
    
    cursor.close()

    stats = {
        'total_students': len(all_students),
        'total_staff': len(all_staff),
        'pending_docs': pending_docs,
        'open_complaints': open_complaints,
        'total_feedbacks': len(feedbacks)
    }

    return render_template('admin-dashboard.html', 
                           student_placements=student_placements,
                           name=session.get('name', 'Master Admin'),
                           user_id=admin_id,
                           college_name=college_name,
                           college_id=college_id,
                           current_admin=current_admin,
                           current_principal=current_principal,
                           all_staff=all_staff,
                           all_students=all_students,
                           electricians=electricians,
                           branches=BRANCHES,
                           years=YEARS,
                           designations=DESIGNATIONS,
                           complaints=complaints, 
                           doc_requests=doc_requests,
                           notices=notices,
                           feedbacks=feedbacks,
                           routine=admin_routine,
                           selected_branch=selected_branch,
                           selected_year=selected_year,
                           stats=stats)

@app.route('/admin/add-staff', methods=['POST'])
def add_staff():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    college_id = session.get('college_id', 'kmbb1234')
    user_id = request.form.get('userId', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    designation = request.form.get('designation')
    branch = request.form.get('branch', '').strip()
    phone = request.form.get('phone', '').strip()
    aadhaar = request.form.get('aadhaar', '').strip()
    bank_account = request.form.get('bank_account', '').strip()
    password = request.form.get('password', '').strip()
    entered_otp = request.form.get('email_otp', '').strip()

    stored_otp = session.get('onboard_otp')
    stored_email = session.get('onboard_email')

    if not stored_otp or entered_otp != stored_otp or email != stored_email:
        flash('❌ Invalid or Missing Email OTP!', 'error')
        return redirect(url_for('admin_dashboard'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s OR email = %s", (user_id, email))
    if cursor.fetchone():
        cursor.close()
        flash('Faculty/Staff ID or Email already exists!', 'error')
        return redirect(url_for('admin_dashboard'))

    photo_url = None
    if 'photo' in request.files and request.files['photo'].filename != '':
        file = request.files['photo']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"staff_{user_id}_{int(datetime.now().timestamp())}.{ext}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = url_for('static', filename=f'uploads/{filename}')

    cursor.execute("""
        INSERT INTO users (user_id, name, email, role, password, status, designation, branch, phone, aadhaar, bank_account, college_id, photo_url)
        VALUES (%s, %s, %s, 'teacher', %s, 'approved', %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, name, email, password, designation, branch, phone, aadhaar, bank_account, college_id, photo_url))
    mysql.connection.commit()
    cursor.close()

    session.pop('onboard_otp', None)
    session.pop('onboard_email', None)
    flash(f'✅ {name} ({designation}) onboarded successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-student', methods=['POST'])
def add_student():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    college_id = session.get('college_id', 'kmbb1234')
    user_id = request.form.get('userId', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    branch = request.form.get('branch')
    year = request.form.get('year')
    password = request.form.get('password', '').strip()
    phone = request.form.get('phone', '').strip()
    aadhaar = request.form.get('aadhaar', '').strip()
    bank_account = request.form.get('bank_account', '').strip()
    father_name = request.form.get('father_name', '').strip()
    mother_name = request.form.get('mother_name', '').strip()
    entered_otp = request.form.get('email_otp', '').strip()

    stored_otp = session.get('onboard_otp')
    stored_email = session.get('onboard_email')
    if not stored_otp or entered_otp != stored_otp or email != stored_email:
        flash('❌ Invalid or Missing Email OTP!', 'error')
        return redirect(url_for('admin_dashboard'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s OR email = %s", (user_id, email))
    if cursor.fetchone():
        cursor.close()
        flash('Student ID or Email already exists!', 'error')
        return redirect(url_for('admin_dashboard'))

    photo_url = None
    if 'photo' in request.files and request.files['photo'].filename != '':
        file = request.files['photo']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"student_{user_id}_{int(datetime.now().timestamp())}.{ext}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = url_for('static', filename=f'uploads/{filename}')

    cursor.execute("""
        INSERT INTO users (user_id, name, email, role, password, status, branch, year, phone, aadhaar, bank_account, father_name, mother_name, college_id, photo_url)
        VALUES (%s, %s, %s, 'student', %s, 'approved', %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, name, email, password, branch, year, phone, aadhaar, bank_account, father_name, mother_name, college_id, photo_url))

    cursor.execute("SELECT user_id FROM users WHERE role = 'teacher' AND designation = 'Hostel Warden' AND college_id = %s", (college_id,))
    wardens = cursor.fetchall()
    for w in wardens:
        notice_title = f"New Student Admission: {name}"
        notice_desc = f"New student {name} (Roll: {user_id}, Branch: {branch}, Year: {year}) has been admitted. Please assign hostel, floor, and room number."
        cursor.execute("""
            INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role)
            VALUES (%s, 'New Student Hostel Allocation', %s, 'Admin Office', %s, %s, 'admin')
        """, (notice_title, notice_desc, w['user_id'], session.get('user_id')))

    mysql.connection.commit()
    cursor.close()

    session.pop('onboard_otp', None)
    session.pop('onboard_email', None)
    flash(f'🎓 Student {name} admitted successfully & warden notified for hostel allocation!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-student', methods=['POST'])
def edit_student():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    user_id = request.form.get('userId', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    branch = request.form.get('branch')
    year = request.form.get('year')
    phone = request.form.get('phone', '').strip()
    aadhaar = request.form.get('aadhaar', '').strip()
    bank_account = request.form.get('bank_account', '').strip()
    father_name = request.form.get('father_name', '').strip()
    mother_name = request.form.get('mother_name', '').strip()
    password = request.form.get('password', '').strip()

    cursor = mysql.connection.cursor()

    if 'photo' in request.files and request.files['photo'].filename != '':
        file = request.files['photo']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"student_{user_id}_{int(datetime.now().timestamp())}.{ext}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = url_for('static', filename=f'uploads/{filename}')

            cursor.execute("""
                UPDATE users SET name=%s, email=%s, branch=%s, year=%s, phone=%s, aadhaar=%s, 
                bank_account=%s, father_name=%s, mother_name=%s, password=%s, photo_url=%s WHERE user_id=%s
            """, (name, email, branch, year, phone, aadhaar, bank_account, father_name, mother_name, password, photo_url, user_id))
    else:
        cursor.execute("""
            UPDATE users SET name=%s, email=%s, branch=%s, year=%s, phone=%s, aadhaar=%s, 
            bank_account=%s, father_name=%s, mother_name=%s, password=%s WHERE user_id=%s
        """, (name, email, branch, year, phone, aadhaar, bank_account, father_name, mother_name, password, user_id))

    mysql.connection.commit()
    cursor.close()

    flash(f'✅ Student {name} profile updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-staff', methods=['POST'])
def edit_staff():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    user_id = request.form.get('userId', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    designation = request.form.get('designation')
    branch = request.form.get('branch', '').strip()
    phone = request.form.get('phone', '').strip()
    aadhaar = request.form.get('aadhaar', '').strip()
    bank_account = request.form.get('bank_account', '').strip()
    password = request.form.get('password', '').strip()

    cursor = mysql.connection.cursor()

    if 'photo' in request.files and request.files['photo'].filename != '':
        file = request.files['photo']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"staff_{user_id}_{int(datetime.now().timestamp())}.{ext}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = url_for('static', filename=f'uploads/{filename}')

            cursor.execute("""
                UPDATE users SET name=%s, email=%s, designation=%s, branch=%s, phone=%s, aadhaar=%s, 
                bank_account=%s, password=%s, photo_url=%s WHERE user_id=%s
            """, (name, email, designation, branch, phone, aadhaar, bank_account, password, photo_url, user_id))
    else:
        cursor.execute("""
            UPDATE users SET name=%s, email=%s, designation=%s, branch=%s, phone=%s, aadhaar=%s, 
            bank_account=%s, password=%s WHERE user_id=%s
        """, (name, email, designation, branch, phone, aadhaar, bank_account, password, user_id))

    mysql.connection.commit()
    cursor.close()

    flash(f'✅ {name} profile updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-user/<string:user_id>')
def delete_user(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    if user_id == session['user_id']:
        flash('❌ Master Admin cannot be deleted!', 'error')
        return redirect(url_for('admin_dashboard'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    mysql.connection.commit()
    cursor.close()

    flash(f'🗑️ User {user_id} deleted permanently!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update-college-profile', methods=['POST'])
def update_college_profile():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    college_id = session.get('college_id', 'kmbb1234')
    new_name = request.form.get('college_name', '').strip()

    if new_name:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE colleges SET college_name = %s WHERE college_id = %s", (new_name, college_id))
        mysql.connection.commit()
        cursor.close()
        session['college_name'] = new_name
        flash(f'🏛️ College Name updated to: {new_name}', 'success')

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/transfer-role', methods=['POST'])
def transfer_role():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    transfer_type = request.form.get('transfer_type')
    new_name = request.form.get('new_name', '').strip()
    new_email = request.form.get('new_email', '').strip().lower()
    new_phone = request.form.get('new_phone', '').strip()
    new_password = request.form.get('new_password', '').strip()
    new_aadhaar = request.form.get('new_aadhaar', '').strip()
    new_bank = request.form.get('new_bank', '').strip()
    entered_otp = request.form.get('email_otp', '').strip()

    stored_otp = session.get('onboard_otp')
    stored_email = session.get('onboard_email')

    if not stored_otp or entered_otp != stored_otp or new_email != stored_email:
        flash('❌ Invalid or Missing Handover OTP!', 'error')
        return redirect(url_for('admin_dashboard'))

    cursor = mysql.connection.cursor()

    if transfer_type == 'admin':
        current_admin_id = session['user_id']
        cursor.execute("""
            UPDATE users 
            SET name = %s, email = %s, phone = %s, password = %s 
            WHERE user_id = %s AND role = 'admin'
        """, (new_name, new_email, new_phone, new_password, current_admin_id))
        mysql.connection.commit()
        cursor.close()

        session.pop('onboard_otp', None)
        session.pop('onboard_email', None)
        session.clear()

        flash(f'🏛️ Admin role successfully transferred!', 'success')
        return redirect(url_for('login'))

    elif transfer_type == 'principal':
        cursor.execute("SELECT * FROM users WHERE designation = 'Principal' LIMIT 1")
        existing_principal = cursor.fetchone()

        if existing_principal:
            cursor.execute("""
                UPDATE users 
                SET name = %s, email = %s, phone = %s, password = %s, aadhaar = %s, bank_account = %s 
                WHERE user_id = %s
            """, (new_name, new_email, new_phone, new_password, new_aadhaar, new_bank, existing_principal['user_id']))
        else:
            principal_id = "principal01"
            cursor.execute("""
                INSERT INTO users (user_id, name, email, role, password, status, designation, phone, aadhaar, bank_account, college_id)
                VALUES (%s, %s, %s, 'teacher', %s, 'approved', 'Principal', %s, %s, %s, %s)
            """, (principal_id, new_name, new_email, new_password, new_phone, new_aadhaar, new_bank, session.get('college_id', 'kmbb1234')))

        mysql.connection.commit()
        cursor.close()

        session.pop('onboard_otp', None)
        session.pop('onboard_email', None)
        flash('👑 Principal role successfully transferred & updated!', 'success')
        return redirect(url_for('admin_dashboard'))

    cursor.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/update-timetable-entry', methods=['POST'])
def update_timetable_entry():
    user_role = session.get('role')
    user_desig = session.get('designation', '')

    if user_role != 'admin' and user_desig != 'Examination Cell / Controller':
        return redirect(url_for('home'))

    branch = request.form.get('branch')
    year = request.form.get('year')
    day_name = request.form.get('day_name')
    p1 = request.form.get('period1', '').strip()
    p2 = request.form.get('period2', '').strip()
    p3 = request.form.get('period3', '').strip()
    p4 = request.form.get('period4', '').strip()
    p5 = request.form.get('period5', '').strip()
    p6 = request.form.get('period6', '').strip()

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO timetables (branch, year, day_name, period1, period2, period3, period4, period5, period6)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            period1 = VALUES(period1), period2 = VALUES(period2), period3 = VALUES(period3),
            period4 = VALUES(period4), period5 = VALUES(period5), period6 = VALUES(period6)
    """, (branch, year, day_name, p1, p2, p3, p4, p5, p6))
    mysql.connection.commit()
    cursor.close()

    flash(f'✅ Timetable updated!', 'success')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('teacher_dashboard', branch=branch, year=year))

@app.route('/submit-exam-marks-batch', methods=['POST'])
def submit_exam_marks_batch():
    user_role = session.get('role')
    user_desig = session.get('designation', '')

    if user_role != 'admin' and user_desig != 'Examination Cell / Controller':
        return redirect(url_for('home'))

    student_id = request.form.get('student_id', '').strip()
    exam_type = request.form.get('exam_type', '').strip()
    subject_count = int(request.form.get('subject_count', 0))
    entered_by = session.get('name', 'Examination Controller')

    cursor = mysql.connection.cursor()
    saved_subjects = 0

    for i in range(1, subject_count + 1):
        sub_name = request.form.get(f'subject_name_{i}', '').strip()
        full_marks_val = request.form.get(f'full_marks_{i}', '').strip()
        secured_marks_val = request.form.get(f'secured_marks_{i}', '').strip()

        if sub_name and full_marks_val and secured_marks_val:
            try:
                full_marks = int(full_marks_val)
                secured = int(secured_marks_val)
            except ValueError:
                continue

            if secured > full_marks:
                secured = full_marks

            pct = round((secured / full_marks) * 100, 2) if full_marks > 0 else 0.0

            if pct >= 90:
                grade = 'O'
            elif pct >= 80:
                grade = 'A+'
            elif pct >= 70:
                grade = 'A'
            elif pct >= 60:
                grade = 'B+'
            elif pct >= 50:
                grade = 'B'
            elif pct >= 40:
                grade = 'P'
            else:
                grade = 'F'

            cursor.execute("""
                INSERT INTO exam_marks (student_id, exam_type, subject, full_marks, secured_marks, percentage, grade, entered_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (student_id, exam_type, sub_name, full_marks, secured, pct, grade, entered_by))
            saved_subjects += 1

    mysql.connection.commit()
    cursor.close()

    flash(f'✅ Marks uploaded successfully!', 'success')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('teacher_dashboard'))

@app.route('/delete-exam-mark/<int:mark_id>')
def delete_exam_mark(mark_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_role = session.get('role')
    user_desig = session.get('designation', '')
    user_id = session.get('user_id')

    cursor = mysql.connection.cursor()
    if user_role == 'admin' or user_desig == 'Examination Cell / Controller':
        cursor.execute("DELETE FROM exam_marks WHERE id = %s", (mark_id,))
    elif user_role == 'student':
        cursor.execute("DELETE FROM exam_marks WHERE id = %s AND student_id = %s", (mark_id, user_id))

    mysql.connection.commit()
    cursor.close()

    flash('🗑️ Exam mark record deleted successfully!', 'success')
    if user_role == 'student':
        return redirect(url_for('student_dashboard'))
    elif user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('teacher_dashboard'))

@app.route('/delete-all-exam-marks')
def delete_all_exam_marks():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_role = session.get('role')
    user_desig = session.get('designation', '')
    user_id = session.get('user_id')

    cursor = mysql.connection.cursor()
    if user_role == 'student':
        cursor.execute("DELETE FROM exam_marks WHERE student_id = %s", (user_id,))
    elif user_role == 'admin' or user_desig == 'Examination Cell / Controller':
        cursor.execute("DELETE FROM exam_marks")

    mysql.connection.commit()
    cursor.close()

    flash('🗑️ Examination marks cleared!', 'success')
    if user_role == 'student':
        return redirect(url_for('student_dashboard'))
    elif user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('teacher_dashboard'))

@app.route('/send-message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    sender_id = session['user_id']
    sender_name = session['name']
    sender_role = session['role']
    user_desig = session.get('designation', '')

    recipient_id = request.form.get('recipient_id')
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', 'Direct Message')

    posted_by = f"{sender_name} ({user_desig if user_desig else sender_role.capitalize()})"

    cursor = mysql.connection.cursor()
    if recipient_id == 'all':
        if sender_role in ['admin', 'teacher']:
            cursor.execute("""
                INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role) 
                VALUES (%s, %s, %s, %s, NULL, %s, %s)
            """, (title, category, description, posted_by, sender_id, sender_role))
            flash('📢 Notice dispatched to entire campus!', 'success')
        else:
            flash('❌ Students can only send direct messages.', 'error')
    else:
        cursor.execute("""
            INSERT INTO notices (title, category, description, posted_by, recipient_id, sender_id, sender_role) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, category, description, posted_by, recipient_id, sender_id, sender_role))
        flash(f'🔒 Private message sent successfully!', 'success')

    mysql.connection.commit()
    cursor.close()

    if user_desig == 'Library Staff / Librarian':
        return redirect(url_for('librarian_dashboard'))
    elif user_desig == 'Accountant / Clerk':
        return redirect(url_for('accountant_dashboard'))
    elif sender_role == 'student':
        return redirect(url_for('student_dashboard'))
    elif sender_role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/delete-notice/<int:notice_id>')
def delete_notice(notice_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']
    user_desig = session.get('designation', '')

    cursor = mysql.connection.cursor()
    if role == 'admin':
        cursor.execute("DELETE FROM notices WHERE id = %s", (notice_id,))
    elif role == 'teacher':
        cursor.execute("DELETE FROM notices WHERE id = %s AND (recipient_id = %s OR sender_id = %s OR recipient_id IS NULL)", (notice_id, user_id, user_id))
    elif role == 'student':
        cursor.execute("DELETE FROM notices WHERE id = %s AND (recipient_id = %s OR recipient_id IS NULL)", (notice_id, user_id))

    mysql.connection.commit()
    cursor.close()

    flash('🗑️ Notice/Message deleted successfully!', 'success')
    if user_desig == 'Library Staff / Librarian':
        return redirect(url_for('librarian_dashboard'))
    elif user_desig == 'Accountant / Clerk':
        return redirect(url_for('accountant_dashboard'))
    elif role == 'student':
        return redirect(url_for('student_dashboard'))
    elif role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/delete-request/<int:req_id>')
def delete_request(req_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    cursor = mysql.connection.cursor()
    if role == 'student':
        cursor.execute("UPDATE requests SET student_hidden = TRUE WHERE id = %s AND student_id = %s", (req_id, user_id))
    elif role == 'teacher':
        cursor.execute("UPDATE requests SET teacher_hidden = TRUE WHERE id = %s AND assigned_to = %s", (req_id, user_id))
    elif role == 'admin':
        cursor.execute("UPDATE requests SET admin_hidden = TRUE WHERE id = %s", (req_id,))

    mysql.connection.commit()
    cursor.close()

    flash('🗑 Request entry deleted successfully!', 'success')
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    elif role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/delete-doc-request/<int:doc_id>')
def delete_doc_request(doc_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    cursor = mysql.connection.cursor()
    if role == 'student':
        cursor.execute("DELETE FROM document_requests WHERE id = %s AND student_id = %s", (doc_id, user_id))
    elif role == 'admin':
        cursor.execute("DELETE FROM document_requests WHERE id = %s", (doc_id,))

    mysql.connection.commit()
    cursor.close()

    flash('🗑️ Certificate record deleted successfully!', 'success')
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/delete-complaint/<int:comp_id>')
def delete_complaint(comp_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    cursor = mysql.connection.cursor()
    if role == 'student':
        cursor.execute("DELETE FROM complaints WHERE id = %s AND student_id = %s", (comp_id, user_id))
    elif role == 'admin':
        cursor.execute("DELETE FROM complaints WHERE id = %s", (comp_id,))

    mysql.connection.commit()
    cursor.close()

    flash('🗑️ Complaint record deleted successfully!', 'success')
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/delete-feedback/<int:fb_id>')
def delete_feedback(fb_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    cursor = mysql.connection.cursor()
    if role == 'student':
        cursor.execute("DELETE FROM mess_feedback WHERE id = %s AND student_id = %s", (fb_id, user_id))
    elif role == 'admin':
        cursor.execute("DELETE FROM mess_feedback WHERE id = %s", (fb_id,))

    mysql.connection.commit()
    cursor.close()

    flash('🗑 Mess feedback deleted from records!', 'success')
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('admin_dashboard'))

@app.route('/update-complaint/<int:comp_id>/<string:status>')
def update_complaint(comp_id, status):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    if status in ['in_progress', 'resolved']:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE complaints SET status = %s WHERE id = %s", (status, comp_id))
        mysql.connection.commit()
        cursor.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/update-doc-request/<int:doc_id>/<string:status>')
def update_doc_request(doc_id, status):
    role = session.get('role')
    if role not in ['admin', 'teacher']:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    valid_statuses = ['Pending Principal', 'Pending Admin', 'Approved', 'ready_to_collect', 'rejected']
    if status in valid_statuses:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE document_requests SET status = %s WHERE id = %s", (status, doc_id))
        mysql.connection.commit()
        cursor.close()
        flash(f'Certificate application marked as {status}!', 'success')

    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('teacher_dashboard'))

@app.route('/download-certificate/<int:doc_id>')
def download_certificate(doc_id):
    if session.get('role') != 'student':
        return redirect(url_for('login'))
        
    student_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT d.*, u.name as student_name, u.branch, u.year 
        FROM document_requests d 
        JOIN users u ON d.student_id = u.user_id 
        WHERE d.id = %s AND d.student_id = %s AND d.status = 'Approved'
    """, (doc_id, student_id))
    doc = cursor.fetchone()
    cursor.close()
    
    if not doc:
        flash('Certificate not found or not yet approved.', 'error')
        return redirect(url_for('student_dashboard'))
        
    return render_template('print_certificate.html', doc=doc, date=datetime.now().strftime('%d %B %Y'))

# =========================================================
# PLACEMENT & INTERNSHIP TRACKING
# =========================================================
@app.route('/submit-placement', methods=['POST'])
def submit_placement():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
        
    student_id = session.get('user_id')
    company_name = request.form.get('company_name')
    role = request.form.get('role')
    package_lpa = request.form.get('package_lpa')
    type = request.form.get('type')
    
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO student_placements (student_id, company_name, role, package_lpa, type, status)
        VALUES (%s, %s, %s, %s, %s, 'Pending')
    """, (student_id, company_name, role, package_lpa, type))
    mysql.connection.commit()
    cursor.close()
    
    flash('Placement/Internship details submitted successfully. Pending verification.', 'success')
    return redirect(url_for('student_dashboard'))


@app.route('/verify-placement/<int:placement_id>/<status>')
def verify_placement(placement_id, status):
    role = session.get('role')
    designation = session.get('designation')
    
    if role != 'admin' and not (role == 'teacher' and designation == 'Principal'):
        flash('Unauthorized! Only Principal or Admin can perform this action.', 'error')
        return redirect(url_for('login'))
        
    if status not in ['Verified', 'Pending', 'Delete']:
        flash('Invalid status action.', 'error')
        return redirect(request.referrer)
        
    cursor = mysql.connection.cursor()
    if status == 'Delete':
        cursor.execute("DELETE FROM student_placements WHERE id = %s", (placement_id,))
        flash('Placement record deleted.', 'success')
    else:
        cursor.execute("UPDATE student_placements SET status = %s WHERE id = %s", (status, placement_id))
        flash(f'Placement record marked as {status}.', 'success')
        
    mysql.connection.commit()
    cursor.close()
    
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(debug=True)
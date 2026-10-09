CREATE DATABASE IF NOT EXISTS campus_connect;
USE campus_connect;

-- Users Table (Email column added for OTP & Reset Password)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('student', 'teacher', 'admin') NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Leave & Gate Pass Requests Table
CREATE TABLE IF NOT EXISTS requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    type ENUM('leave', 'gate_pass') NOT NULL,
    reason TEXT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Complaints Table
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('open', 'in_progress', 'resolved') DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Notices Table
CREATE TABLE IF NOT EXISTS notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    posted_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Default Demo Logins (With emails)
INSERT INTO users (user_id, name, email, role, password) VALUES
('stu01', 'Rahul Kumar', 'student.demo@gmail.com', 'student', 'student123'),
('teach01', 'Prof. Sharma', 'teacher.demo@gmail.com', 'teacher', 'teacher123'),
('admin01', 'System Admin', 'admin.demo@gmail.com', 'admin', 'admin123')
ON DUPLICATE KEY UPDATE email=VALUES(email);

SELECT * FROM users;

USE campus_connect;

-- 1. Purane 'users' table mein email ka column add karein
ALTER TABLE users ADD COLUMN email VARCHAR(100) UNIQUE AFTER name;

-- 2. Purane demo users ko valid email assign karein (Testing ke liye)
UPDATE users SET email = 'student.demo@gmail.com' WHERE user_id = 'stu01';
UPDATE users SET email = 'teacher.demo@gmail.com' WHERE user_id = 'teach01';
UPDATE users SET email = 'admin.demo@gmail.com' WHERE user_id = 'admin01';

USE campus_connect;

-- 1. Daily Mess Menu Table
CREATE TABLE IF NOT EXISTS mess_menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day_name VARCHAR(20) NOT NULL,
    breakfast TEXT NOT NULL,
    lunch TEXT NOT NULL,
    snacks TEXT NOT NULL,
    dinner TEXT NOT NULL
);

-- Demo Menu Insert
INSERT INTO mess_menu (day_name, breakfast, lunch, snacks, dinner) VALUES
('Today', 'Aloo Paratha, Curd, Tea', 'Rice, Dal, Paneer Butter Masala, Salad', 'Samosa, Tea', 'Roti, Mixed Veg, Dal Fry, Kheer')
ON DUPLICATE KEY UPDATE breakfast=VALUES(breakfast);

-- 2. Student Mess Feedback Table
CREATE TABLE IF NOT EXISTS mess_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    meal_type ENUM('breakfast', 'lunch', 'snacks', 'dinner') NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);

USE campus_connect;

-- Document & Certificate Requests Table
CREATE TABLE IF NOT EXISTS document_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    doc_type ENUM('bonafide', 'fee_due', 'character_cert', 'hostel_noc') NOT NULL,
    purpose TEXT NOT NULL,
    status VARCHAR(100) DEFAULT 'Pending HOD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);

USE campus_connect;
ALTER TABLE notices ADD COLUMN category VARCHAR(50) DEFAULT 'All Campus' AFTER title;

SELECT * FROM notices;

USE campus_connect;

-- 1. Pehle student ko users table mein add karein
INSERT INTO users (user_id, name, email, role, password) 
VALUES ('220101', 'Jayant sharma', 'jayant@student.edu', 'student', 'student123')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 2. Ab 6 subjects ki attendance daalein
INSERT INTO attendance (student_id, subject, date, status, marked_by) VALUES
('220101', 'Data Structures & Algorithms', CURDATE(), 'Present', 'Faculty'),
('220101', 'Database Management Systems', CURDATE(), 'Present', 'Faculty'),
('220101', 'Operating Systems', CURDATE(), 'Present', 'Faculty'),
('220101', 'Computer Networks', CURDATE(), 'Absent', 'Faculty'),
('220101', 'Software Engineering', CURDATE(), 'Present', 'Faculty'),
('220101', 'Artificial Intelligence', CURDATE(), 'Present', 'Faculty'),

('220101', 'Data Structures & Algorithms', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', 'Faculty'),
('220101', 'Database Management Systems', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', 'Faculty'),
('220101', 'Operating Systems', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Absent', 'Faculty'),
('220101', 'Computer Networks', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', 'Faculty'),
('220101', 'Software Engineering', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', 'Faculty'),
('220101', 'Artificial Intelligence', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', 'Faculty');


USE campus_connect;

ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'pending_approval';
UPDATE users SET status = 'approved';


SET SQL_SAFE_UPDATES = 0;

UPDATE users SET status = 'approved';

SET SQL_SAFE_UPDATES = 1;



USE campus_connect;

-- Users table mein designation aur staff details columns add karein
ALTER TABLE users 
ADD COLUMN designation VARCHAR(100) DEFAULT 'Staff',
ADD COLUMN phone VARCHAR(20) DEFAULT NULL,
ADD COLUMN aadhaar VARCHAR(20) DEFAULT NULL,
ADD COLUMN bank_account VARCHAR(50) DEFAULT NULL,
ADD COLUMN photo_url TEXT DEFAULT NULL;

-- Notices table mein recipient_id add karein specific messages ke liye
ALTER TABLE notices 
ADD COLUMN recipient_id VARCHAR(50) DEFAULT NULL;


USE campus_connect;

-- 1. Document / Certificate Requests Table
CREATE TABLE IF NOT EXISTS document_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    doc_type VARCHAR(100) NOT NULL,
    purpose TEXT NOT NULL,
    status ENUM('pending', 'approved', 'ready_to_collect', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 2. Hostel Mess Feedback Table
CREATE TABLE IF NOT EXISTS mess_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    meal_type VARCHAR(50) NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 3. Hostel Mess Menu Table (Daily Menu)
CREATE TABLE IF NOT EXISTS mess_menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    breakfast VARCHAR(255) DEFAULT 'Aloo Paratha, Curd, Tea',
    lunch VARCHAR(255) DEFAULT 'Rice, Dal, Paneer Butter Masala, Salad',
    snacks VARCHAR(255) DEFAULT 'Samosa, Masala Chai',
    dinner VARCHAR(255) DEFAULT 'Roti, Mixed Veg, Kheer'
);

INSERT INTO mess_menu (breakfast, lunch, snacks, dinner) 
VALUES ('Aloo Paratha, Curd, Tea', 'Rice, Dal, Paneer Butter Masala, Salad', 'Samosa, Masala Chai', 'Roti, Mixed Veg, Kheer')
ON DUPLICATE KEY UPDATE id=id;


USE campus_connect;

-- Purani table ko refresh karke sahi columns set karein
DROP TABLE IF EXISTS mess_menu;

CREATE TABLE mess_menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day_name VARCHAR(50) DEFAULT 'Today',
    breakfast VARCHAR(255) DEFAULT 'Aloo Paratha, Curd, Tea',
    lunch VARCHAR(255) DEFAULT 'Rice, Dal, Paneer Butter Masala, Salad',
    snacks VARCHAR(255) DEFAULT 'Samosa, Masala Chai',
    dinner VARCHAR(255) DEFAULT 'Roti, Mixed Veg, Kheer'
);

-- Default data insert karein
INSERT INTO mess_menu (day_name, breakfast, lunch, snacks, dinner) 
VALUES ('Today', 'Aloo Paratha, Curd, Tea', 'Rice, Dal, Paneer Butter Masala, Salad', 'Samosa, Masala Chai', 'Roti, Mixed Veg, Kheer');



USE campus_connect;

ALTER TABLE notices 
ADD COLUMN IF NOT EXISTS sender_id VARCHAR(50) NULL AFTER posted_by,
ADD COLUMN IF NOT EXISTS sender_role VARCHAR(20) NULL AFTER sender_id;


USE campus_connect;

ALTER TABLE notices 
ADD COLUMN sender_id VARCHAR(50) NULL AFTER posted_by,
ADD COLUMN sender_role VARCHAR(20) NULL AFTER sender_id;

USE campus_connect;

ALTER TABLE requests 
ADD COLUMN assigned_to VARCHAR(50) NULL AFTER student_id;


USE campus_connect;

-- Add branch and year columns to users table
ALTER TABLE users 
ADD COLUMN branch VARCHAR(20) DEFAULT 'CSE' AFTER designation,
ADD COLUMN year VARCHAR(20) DEFAULT '1st Year' AFTER branch;

-- Existing students ko default set karein
UPDATE users SET branch = 'CSE', year = '2nd Year' WHERE role = 'student' AND (branch IS NULL OR branch = '');


USE campus_connect;

SET SQL_SAFE_UPDATES = 0;

UPDATE users 
SET branch = 'CSE', year = '2nd Year' 
WHERE role = 'student' AND (branch IS NULL OR branch = '' OR branch = 'CSE');

SET SQL_SAFE_UPDATES = 1;





USE campus_connect;

SET SQL_SAFE_UPDATES = 0;

-- 1. Ensure mess_feedback table has 'day_name' column
ALTER TABLE mess_feedback 
ADD COLUMN day_name VARCHAR(20) DEFAULT 'Today' AFTER student_id;

-- 2. Recreate mess_menu table with all 7 days of the week
DROP TABLE IF EXISTS mess_menu;
CREATE TABLE mess_menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day_name VARCHAR(20) NOT NULL UNIQUE,
    breakfast VARCHAR(255) NOT NULL,
    lunch VARCHAR(255) NOT NULL,
    snacks VARCHAR(255) NOT NULL,
    dinner VARCHAR(255) NOT NULL
);

-- 3. Insert 7 Days Complete Indian College Hostel Menu
INSERT INTO mess_menu (day_name, breakfast, lunch, snacks, dinner) VALUES
('Monday', 'Idli, Sambar, Coconut Chutney, Tea/Coffee', 'Rice, Dal Fry, Seasonal Mixed Veg, Curd, Salad', 'Samosa, Green Chutney, Masala Chai', 'Roti, Paneer Butter Masala, Jeera Rice, Gulab Jamun'),
('Tuesday', 'Aloo Paratha, Curd, Butter, Pickle, Tea', 'Rice, Rajma Masala, Aloo Jeera, Papad, Salad', 'Veg Cutlet, Tomato Sauce, Tea', 'Roti, Dal Tadka, Seasonal Sabzi, Rice, Kheer'),
('Wednesday', 'Poha, Sev, Boiled Eggs / Banana, Tea', 'Rice, Yellow Dal, Egg Curry / Paneer Bhurji, Salad', 'Biscuits, Namkeen, Coffee/Tea', 'Roti, Chana Masala, Veg Pulao, Raita, Ice Cream'),
('Thursday', 'Uttapam / Dosa, Sambar, Chutney, Tea', 'Rice, Kadhi Pakoda, Aloo Gobhi, Pickle, Papad', 'Bread Pakoda, Mint Chutney, Tea', 'Roti, Mix Veg Korma, Dal Makhani, Steamed Rice, Fruit Custard'),
('Friday', 'Methi Paratha, Curd, Pickle, Tea/Coffee', 'Rice, Chana Dal, Bhindi Fry, Boondi Raita, Salad', 'Pani Puri / Chaat, Tea', 'Special Veg Biryani / Chicken Biryani, Salan, Raita, Rasgulla'),
('Saturday', 'Puri Sabzi (Aloo Tamatar), Halwa, Tea', 'Khichdi, Baingan Bhaja, Papad, Pickle, Curd', 'Pasta / Maggi, Cold Drink / Tea', 'Roti, Dal Tadka, Dum Aloo, Jeera Rice, Sweet Seviyan'),
('Sunday', 'Masala Dosa / Chhole Bhature, Special Tea', 'Special Veg Thali (Paneer, Dal, Pulao, Puri, Raita)', 'Pakauda (Onion/Potato), Adrak Chai', 'Roti, Shahi Paneer, Fried Rice, Dal, Hot Gulab Jamun');

SET SQL_SAFE_UPDATES = 1;


USE campus_connect;

ALTER TABLE users 
ADD COLUMN father_name VARCHAR(100) NULL AFTER bank_account,
ADD COLUMN mother_name VARCHAR(100) NULL AFTER father_name;






USE campus_connect;

DROP TABLE IF EXISTS timetables;
CREATE TABLE timetables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    branch VARCHAR(20) NOT NULL,
    year VARCHAR(20) NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    period1 VARCHAR(100) NOT NULL,
    period2 VARCHAR(100) NOT NULL,
    period3 VARCHAR(100) NOT NULL,
    period4 VARCHAR(100) NOT NULL,
    period5 VARCHAR(100) NOT NULL,
    period6 VARCHAR(100) NOT NULL,
    UNIQUE KEY branch_year_day (branch, year, day_name)
);


USE campus_connect;

ALTER TABLE document_requests MODIFY COLUMN doc_type VARCHAR(100) NOT NULL;


USE campus_connect;

CREATE TABLE IF NOT EXISTS exam_marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    exam_type VARCHAR(50) NOT NULL, -- e.g. 'Internal Assessment' or 'Semester Examination'
    subject VARCHAR(150) NOT NULL,
    full_marks INT NOT NULL,
    secured_marks INT NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    grade VARCHAR(10) NOT NULL,
    remarks VARCHAR(255) DEFAULT 'Published',
    entered_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);


USE campus_connect;

ALTER TABLE exam_marks MODIFY COLUMN grade VARCHAR(50) NOT NULL;


USE campus_connect;

-- 1. Create Colleges Table
CREATE TABLE IF NOT EXISTS colleges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id VARCHAR(50) NOT NULL UNIQUE,
    college_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Insert KMBB as Default Primary College
INSERT INTO colleges (college_id, college_name) 
VALUES ('kmbb1234', 'KMBB College of Engineering and Technology')
ON DUPLICATE KEY UPDATE college_name=VALUES(college_name);

-- 3. Add college_id to users and link all existing data to KMBB
ALTER TABLE users ADD COLUMN college_id VARCHAR(50) DEFAULT 'kmbb1234' AFTER role;
UPDATE users SET college_id = 'kmbb1234' WHERE college_id IS NULL OR college_id = '';


USE campus_connect;

-- 1. Pehle safe mode off karein
SET SQL_SAFE_UPDATES = 0;

-- 2. Users table mein college_id column add karein
ALTER TABLE users 
ADD COLUMN college_id VARCHAR(50) DEFAULT 'kmbb1234' AFTER role;

-- 3. Abhi ke saare existing users ko KMBB college se link karein
UPDATE users 
SET college_id = 'kmbb1234';

-- 4. Safe mode wapas on karein
SET SQL_SAFE_UPDATES = 1;

-- 5. Verify karein ki column aur data sahi set hua ya nahi
SELECT user_id, name, role, college_id FROM users;


USE campus_connect;
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id VARCHAR(50) DEFAULT 'kmbb1234',
    book_code VARCHAR(50) NOT NULL UNIQUE,
    book_name VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    total_copies INT DEFAULT 5,
    available_copies INT DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- 2. BOOK ISSUES & DUE DATE TRACKING TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS book_issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id VARCHAR(50) DEFAULT 'kmbb1234',
    student_id VARCHAR(50) NOT NULL,
    book_code VARCHAR(50) NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status ENUM('issued', 'returned', 'overdue') DEFAULT 'issued',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (book_code) REFERENCES books(book_code) ON DELETE CASCADE
);

USE campus_connect;

-- Notices table me college_id add karein
ALTER TABLE notices 
ADD COLUMN college_id VARCHAR(50) DEFAULT 'kmbb1234' AFTER id;

-- Existing notices ko KMBB college se link karein
UPDATE notices 
SET college_id = 'kmbb1234' 
WHERE college_id IS NULL OR college_id = '';



USE campus_connect;

-- 1. Safe update mode ko temporarily off karein
SET SQL_SAFE_UPDATES = 0;

-- 2. Notices table me college_id update karein
UPDATE notices 
SET college_id = 'kmbb1234' 
WHERE college_id IS NULL OR college_id = '';

-- 3. Safe update mode ko wapas on karein
SET SQL_SAFE_UPDATES = 1;

-- 4. Check karein ki update ho gaya ya nahi
SELECT id, title, college_id FROM notices LIMIT 5;





USE campus_connect;

-- 1. Books Inventory Table
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id VARCHAR(50) DEFAULT 'kmbb1234',
    book_code VARCHAR(50) NOT NULL UNIQUE,
    book_name VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    total_copies INT DEFAULT 5,
    available_copies INT DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Book Issues Table (Pending, Issued, Returned, Overdue support ke saath)
CREATE TABLE IF NOT EXISTS book_issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id VARCHAR(50) DEFAULT 'kmbb1234',
    student_id VARCHAR(50) NOT NULL,
    book_code VARCHAR(50) NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status ENUM('pending', 'issued', 'returned', 'overdue') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (book_code) REFERENCES books(book_code) ON DELETE CASCADE
);

-- 3. Notices table me college_id add & safe update
ALTER TABLE notices ADD COLUMN IF NOT EXISTS college_id VARCHAR(50) DEFAULT 'kmbb1234' AFTER id;

SET SQL_SAFE_UPDATES = 0;
UPDATE notices SET college_id = 'kmbb1234' WHERE college_id IS NULL OR college_id = '';
SET SQL_SAFE_UPDATES = 1;

USE campus_connect;

-- 1. Book issues table mein status column ko koushin karein (pending option enable karne ke liye)
ALTER TABLE book_issues 
MODIFY COLUMN status ENUM('pending', 'issued', 'returned', 'overdue') DEFAULT 'pending';

-- 2. Safe updates off karein
SET SQL_SAFE_UPDATES = 0;

-- 3. Existing notices ko college_id ke sath sync karein
UPDATE notices 
SET college_id = 'kmbb1234' 
WHERE college_id IS NULL OR college_id = '';

-- 4. Safe updates wapas on karein
SET SQL_SAFE_UPDATES = 1;

-- 5. Verify karein ki sabhi tables aur columns theek hain
SELECT id, title, college_id FROM notices LIMIT 5;
SELECT * FROM book_issues LIMIT 5;





USE campus_connect;

-- =========================================
-- 1. STUDENT FEES STRUCTURE TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS student_fees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id VARCHAR(50) DEFAULT 'kmbb1234',
    student_id VARCHAR(50) NOT NULL,
    semester VARCHAR(50) NOT NULL,
    total_fee DECIMAL(10, 2) NOT NULL DEFAULT 50000.00,
    paid_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    due_fee DECIMAL(10, 2) NOT NULL DEFAULT 50000.00,
    due_date DATE NOT NULL,
    status ENUM('paid', 'partial', 'pending') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =========================================
-- 2. FEE TRANSACTIONS & RECEIPTS TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS fee_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id VARCHAR(50) DEFAULT 'kmbb1234',
    student_id VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_mode ENUM('UPI', 'Cash', 'Net Banking', 'Bank Transfer', 'Cheque') NOT NULL DEFAULT 'UPI',
    transaction_ref_no VARCHAR(100) NOT NULL,
    payment_date DATE NOT NULL,
    remarks VARCHAR(255) DEFAULT 'Semester Fee Payment',
    status ENUM('pending_verification', 'verified', 'rejected') DEFAULT 'pending_verification',
    verified_by VARCHAR(100) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Demo Fees Structure for testing
INSERT INTO student_fees (college_id, student_id, semester, total_fee, paid_fee, due_fee, due_date, status)
SELECT 'kmbb1234', user_id, '1st Semester', 55000.00, 25000.00, 30000.00, DATE_ADD(CURDATE(), INTERVAL 30 DAY), 'partial'
FROM users WHERE role = 'student'
LIMIT 1
ON DUPLICATE KEY UPDATE id=id;


USE campus_connect;

-- Demo Fees Structure for testing (Fix ambiguous column error)
INSERT INTO student_fees (college_id, student_id, semester, total_fee, paid_fee, due_fee, due_date, status)
SELECT 'kmbb1234', user_id, '1st Semester', 55000.00, 25000.00, 30000.00, DATE_ADD(CURDATE(), INTERVAL 30 DAY), 'partial'
FROM users 
WHERE role = 'student'
LIMIT 1;

-- Check check karne ke liye run karein
SELECT * FROM student_fees;     



ALTER DATABASE campus_connect CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

ALTER TABLE notices CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER DATABASE campus_connect CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

ALTER TABLE notices CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE campus_connect;

ALTER TABLE notices CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER DATABASE campus_connect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE campus_connect;

ALTER TABLE notices CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE notices MODIFY description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE notices MODIFY title VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE campus_connect;
ALTER TABLE complaints MODIFY status VARCHAR(50);




USE campus_connect;
ALTER TABLE notices MODIFY COLUMN posted_by VARCHAR(255);

USE campus_connect;
ALTER TABLE complaints MODIFY COLUMN description TEXT;
ALTER TABLE complaints MODIFY COLUMN title VARCHAR(255);

ALTER TABLE notices MODIFY COLUMN description TEXT;
ALTER TABLE notices MODIFY COLUMN title VARCHAR(255);
ALTER TABLE notices MODIFY COLUMN posted_by VARCHAR(255);

ALTER TABLE mess_feedback MODIFY COLUMN comment TEXT;

ALTER TABLE fee_transactions MODIFY COLUMN remarks TEXT;

USE campus_connect;
CREATE TABLE IF NOT EXISTS student_placements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    company_name VARCHAR(150) NOT NULL,
    role VARCHAR(100) NOT NULL,
    package_lpa DECIMAL(5,2) NOT NULL,
    type ENUM('Placement', 'Internship') NOT NULL,
    status ENUM('Pending', 'Verified') DEFAULT 'Pending',
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
);
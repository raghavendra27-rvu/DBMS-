-- Student Record Management System
-- Database Creation

CREATE DATABASE IF NOT EXISTS student_db;

USE student_db;

-- Create Students Table

CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    course VARCHAR(80) NOT NULL,
    semester INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Sample Student Records

INSERT INTO students (name, email, course, semester)
VALUES
('Asha Kumar', 'asha@example.com', 'BCA', 3),
('Rahul Sharma', 'rahul@example.com', 'BCA', 4),
('Priya Reddy', 'priya@example.com', 'BCA', 2),
('Arjun Kumar', 'arjun@example.com', 'BCA', 5),
('Sneha Rao', 'sneha@example.com', 'BCA', 1);

-- Display All Student Records

SELECT * FROM students;

-- Search Student by Name

SELECT * FROM students
WHERE name LIKE '%Asha%';

-- Update Student Details

UPDATE students
SET course = 'BCA Honors', semester = 4
WHERE student_id = 1;

-- Delete Student Record

DELETE FROM students
WHERE student_id = 5;

-- Display Final Student Records

SELECT * FROM students;
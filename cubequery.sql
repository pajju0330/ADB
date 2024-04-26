CREATE DATABASE CUBE;
USE CUBE;
go

CREATE TABLE admissions (
    sid INT,
    cid INT,
    did INT,
    a_date DATE,
    t_fee DECIMAL(10, 2)
);

CREATE TABLE students (
    sid INT PRIMARY KEY,
    sname VARCHAR(100),
    gender VARCHAR(10),
    dob DATE
);

CREATE TABLE courses (
    cid INT PRIMARY KEY,
    cname VARCHAR(100),
    did INT,
    credit_hours INT
);

CREATE TABLE departments (
    did INT PRIMARY KEY,
    dname VARCHAR(100),
    hod VARCHAR(100)
);

INSERT INTO students VALUES (1, 'Prajwal', 'Female', '2003-03-28');
INSERT INTO students VALUES (2, 'Alice', 'Female', '2003-08-07');
INSERT INTO students VALUES (3, 'John', 'Male', '2003-11-15');

INSERT INTO courses VALUES (1, 'Computer Science', 1, 4);
INSERT INTO courses VALUES (2, 'Mathematics', 2, 3);
INSERT INTO courses VALUES (3, 'Biology', 3, 5);

INSERT INTO departments VALUES (1, 'Computer Science', 'Dr. A');
INSERT INTO departments VALUES (2, 'Mathematics', 'Dr. B');
INSERT INTO departments VALUES (3, 'Biology', 'Dr. C');

INSERT INTO admissions VALUES (1, 1, 1, '2023-09-01', 2000.00);
INSERT INTO admissions VALUES (2, 2, 2, '2023-09-01', 1500.00);
INSERT INTO admissions VALUES (3, 1, 1, '2023-09-01', 2200.00);
INSERT INTO admissions VALUES (1, 3, 3, '2023-09-01', 2500.00);
INSERT INTO admissions VALUES (3, 2, 3, '2023-09-01', 1800.00);
INSERT INTO admissions VALUES (3, 3, 2, '2023-09-01', 3000.00);

SELECT
    s.sname,
    c.cname,
    d.dname,
    SUM(a.t_fee) AS total_tuition_fee
FROM
    admissions a
JOIN
    students s ON a.sid = s.sid
JOIN
    courses c ON a.cid = c.cid
JOIN
    departments d ON a.did = d.did
GROUP BY
    CUBE(s.sname, c.cname, d.dname);x
USE company;

-- 1) Departments first (mgr_ssn = NULL for now, employees don't exist yet)
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES
(1, 'Research',       NULL, NULL),
(2, 'Administration', NULL, NULL),
(3, 'Headquarters',   NULL, NULL);

-- 2) Employees (their Dno now exists)
INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES
('111111111', 'Ahmed',  'Hassan', '1985-03-12', 'Alexandria', 'M', 8000.00, 1),
('222222222', 'Mona',   'Ali',    '1990-07-25', 'Cairo',      'F', 7500.00, 2),
('333333333', 'Omar',   'Samir',  '1988-11-02', 'Giza',       'M', 9000.00, 3),
('444444444', 'Nour',   'Khaled', '1995-01-18', 'Alexandria', 'F', 5000.00, 1);

-- 3) Now set the managers of the departments
UPDATE DEPARTMENT SET mgr_ssn = '111111111', mgr_start_date = '2015-01-01' WHERE Dnumber = 1;
UPDATE DEPARTMENT SET mgr_ssn = '222222222', mgr_start_date = '2018-06-15' WHERE Dnumber = 2;
UPDATE DEPARTMENT SET mgr_ssn = '333333333', mgr_start_date = '2020-09-01' WHERE Dnumber = 3;

-- 4) Projects (their Dno exists)
INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES
(10, 'ProductX',      'Alexandria', 1),
(20, 'Reorganization', 'Cairo',     2),
(30, 'Newbenefits',    'Giza',      3);
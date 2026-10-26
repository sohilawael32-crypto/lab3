DROP DATABASE IF EXISTS company;
CREATE DATABASE company;
USE company;

-- 1) Create the tables first, without foreign keys
--    (EMPLOYEE and DEPARTMENT reference each other, so one must exist before the other)

CREATE TABLE EMPLOYEE (
  ssn      CHAR(9)       NOT NULL,
  fname    VARCHAR(30)   NOT NULL,
  lname    VARCHAR(30)   NOT NULL,
  bdate    DATE,
  address  VARCHAR(100),
  gender   CHAR(1),
  salary   DECIMAL(10,2),
  Dno      INT,
  PRIMARY KEY (ssn)
);

CREATE TABLE DEPARTMENT (
  Dnumber        INT          NOT NULL,
  Dname          VARCHAR(50)  NOT NULL,
  mgr_ssn        CHAR(9),
  mgr_start_date DATE,
  PRIMARY KEY (Dnumber)
);

CREATE TABLE PROJECT (
  Pnumber   INT          NOT NULL,
  Pname     VARCHAR(50)  NOT NULL,
  Plocation VARCHAR(50),
  Dno       INT,
  PRIMARY KEY (Pnumber)
);

-- 2) Add the foreign keys afterwards with ALTER TABLE

ALTER TABLE EMPLOYEE
  ADD FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber);

ALTER TABLE DEPARTMENT
  ADD FOREIGN KEY (mgr_ssn) REFERENCES EMPLOYEE(ssn);

ALTER TABLE PROJECT
  ADD FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber);
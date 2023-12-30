CREATE TABLE employees 
(   emp_no INT NOT NULL,
    birth_date DATE NOT NULL,
    first_name VARCHAR(14) NOT NULL,
    last_name VARCHAR(16) NOT NULL,
    gender VARCHAR(1) CHECK(gender IN ('F','M')),    
    hire_date DATE NOT NULL,
    CONSTRAINT pk_emp PRIMARY KEY (emp_no)
);

CREATE TABLE departments (
    dept_no     CHAR(4)         NOT NULL,
    dept_name   VARCHAR(40)     NOT NULL,
    CONSTRAINT pk_dept PRIMARY KEY (dept_no),
    UNIQUE (dept_name)
);

CREATE TABLE dept_manager (
   emp_no       INT             NOT NULL,
   dept_no      CHAR(4)         NOT NULL,
   from_date    DATE            NOT NULL,
   to_date      DATE            NOT NULL,
  CONSTRAINT fk_dept_man_emp
    FOREIGN KEY (emp_no)
    REFERENCES employees(emp_no) ON DELETE CASCADE,
  CONSTRAINT fk_dept_man_dept
    FOREIGN KEY (dept_no)
    REFERENCES departments(dept_no) ON DELETE CASCADE,
  CONSTRAINT pk_dept_man PRIMARY KEY (emp_no,dept_no)
);

CREATE TABLE dept_emp (
    emp_no      INT             NOT NULL,
    dept_no     CHAR(4)         NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE            NOT NULL,
  CONSTRAINT fk_dept_emp_emp
    FOREIGN KEY (emp_no)
    REFERENCES employees(emp_no) ON DELETE CASCADE,
  CONSTRAINT fk_dept_emp_dept
    FOREIGN KEY (dept_no)
    REFERENCES departments(dept_no) ON DELETE CASCADE,
  CONSTRAINT pk_dept_emp PRIMARY KEY (emp_no,dept_no)
);

CREATE TABLE titles (
    emp_no      INT             NOT NULL,
    title       VARCHAR(50)     NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE,
  CONSTRAINT fk_title_emp
    FOREIGN KEY (emp_no)
    REFERENCES employees(emp_no) ON DELETE CASCADE,
  CONSTRAINT pk_title PRIMARY KEY (emp_no,title, from_date)
) 
; 
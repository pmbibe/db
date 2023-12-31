CREATE TABLE titles (
    emp_no      INT             NOT NULL,
    title       VARCHAR(50)     NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE,
  CONSTRAINT fk_title_emp
    FOREIGN KEY (emp_no)
    REFERENCES employees(emp_no) ON DELETE CASCADE,
  CONSTRAINT pk_title PRIMARY KEY (emp_no,title, from_date)
) ; 

INSERT INTO titles VALUES (10001,'Senior Engineer',TO_DATE('1986-06-26','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10002,'Staff',TO_DATE('1996-08-03','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10003,'Senior Engineer',TO_DATE('1995-12-03','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10004,'Engineer',TO_DATE('1986-12-01','YYYY-MM-DD'),TO_DATE('1995-12-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10004,'Senior Engineer',TO_DATE('1995-12-01','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10005,'Senior Staff',TO_DATE('1996-09-12','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10005,'Staff',TO_DATE('1989-09-12','YYYY-MM-DD'),TO_DATE('1996-09-12','YYYY-MM-DD'));
INSERT INTO titles VALUES (10006,'Senior Engineer',TO_DATE('1990-08-05','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10007,'Senior Staff',TO_DATE('1996-02-11','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10007,'Staff',TO_DATE('1989-02-10','YYYY-MM-DD'),TO_DATE('1996-02-11','YYYY-MM-DD'));
INSERT INTO titles VALUES (10008,'Assistant Engineer',TO_DATE('1998-03-11','YYYY-MM-DD'),TO_DATE('2000-07-31','YYYY-MM-DD'));
INSERT INTO titles VALUES (10009,'Assistant Engineer',TO_DATE('1985-02-18','YYYY-MM-DD'),TO_DATE('1990-02-18','YYYY-MM-DD'));
INSERT INTO titles VALUES (10009,'Engineer',TO_DATE('1990-02-18','YYYY-MM-DD'),TO_DATE('1995-02-18','YYYY-MM-DD'));
INSERT INTO titles VALUES (10009,'Senior Engineer',TO_DATE('1995-02-18','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10010,'Engineer',TO_DATE('1996-11-24','YYYY-MM-DD'),TO_DATE('9999-01-01','YYYY-MM-DD'));
INSERT INTO titles VALUES (10011,'Staff',TO_DATE('1990-01-22','YYYY-MM-DD'),TO_DATE('1996-11-09','YYYY-MM-DD'));
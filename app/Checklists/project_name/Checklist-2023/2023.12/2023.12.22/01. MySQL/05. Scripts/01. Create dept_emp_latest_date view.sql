CREATE OR REPLACE VIEW dept_emp_latest_date_01 AS
    SELECT emp_no, MAX(from_date) AS from_date, MAX(to_date) AS to_date
    FROM dept_emp
    GROUP BY emp_no;
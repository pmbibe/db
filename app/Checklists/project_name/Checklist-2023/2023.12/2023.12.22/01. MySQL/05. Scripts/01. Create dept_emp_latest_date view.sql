CREATE OR REPLACE VIEW employees.dept_emp_latest_date AS
    SELECT emp_no, MAX(from_date) AS from_date, MAX(to_date) AS to_date
    FROM employees.dept_emp
    GROUP BY emp_no;
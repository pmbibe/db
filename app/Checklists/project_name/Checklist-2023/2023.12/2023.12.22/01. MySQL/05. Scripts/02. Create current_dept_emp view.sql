CREATE OR REPLACE VIEW employees.current_dept_emp AS
    SELECT l.emp_no, dept_no, l.from_date, l.to_date
    FROM employees.dept_emp d
        INNER JOIN employees.dept_emp_latest_date l
        ON d.emp_no=l.emp_no AND d.from_date=l.from_date AND l.to_date = d.to_date;
CREATE TABLE employees.test_employees (
  EmployeeID INT PRIMARY KEY,
  FirstName VARCHAR(255),
  LastName VARCHAR(255),
  Email VARCHAR(255),
  Phone VARCHAR(255),
  HireDate DATE,
  Salary DECIMAL(10, 2)
);

INSERT INTO employees.test_employees (FirstName, LastName, Email, Phone, HireDate, Salary)
VALUES ('John', 'Doe', 'helloworld0@email.com', '123-456-7890', 2000);

INSERT INTO employees.test_employees (FirstName, LastName, Email, Phone, HireDate, Salary)
VALUES ('John', 'Doe', 'helloworld1@email.com', '123-456-7890', 2000);

INSERT INTO employees.test_employees (FirstName, LastName, Email, Phone, HireDate, Salary)
VALUES ('John', 'Doe', 'helloworld2@email.com', '123-456-7890', 2000);

INSERT INTO employees.test_employees (FirstName, LastName, Email, Phone, HireDate, Salary)
VALUES ('John', 'Doe', 'helloworld3@email.com', '123-456-7890', 2000);

INSERT INTO employees.test_employees (FirstName, LastName, Email, Phone, HireDate, Salary)
VALUES ('John', 'Doe', 'helloworld4@email.com', '123-456-7890', 2000);
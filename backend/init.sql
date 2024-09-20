DROP TABLE IF EXISTS Cafe;
DROP TABLE IF EXISTS Employee;

-- Create the Cafe table
CREATE TABLE Cafe (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),  -- UUID format
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    logo BLOB,  -- Optional to store binary image data for the logo
    location VARCHAR(255) NOT NULL
);

CREATE TABLE Employee (
    id VARCHAR(9) PRIMARY KEY,  -- Format: UIXXXXXXX
    name VARCHAR(100) NOT NULL,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    phone_number CHAR(8) NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    start_date DATE,  -- The date the employee started working at the cafe
    CHECK (email_address REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    CHECK (phone_number REGEXP '^[89][0-9]{7}$'),  -- Ensure phone starts with 8 or 9 and is 8 digits
    cafe_id CHAR(36),  -- Foreign key to the Cafe table
    FOREIGN KEY (cafe_id) REFERENCES Cafe(id),  -- Ensure the cafe exists
    UNIQUE (id, cafe_id)  -- Prevents assigning the same employee to multiple cafes
);

DELIMITER //

CREATE TRIGGER before_employee_insert
BEFORE INSERT ON Employee
FOR EACH ROW
BEGIN
    -- Check if the id is null or empty, then generate one
    IF NEW.id IS NULL THEN
        -- Generate a random 7-character alphanumeric string, prefix it with 'UI'
        SET NEW.id = CONCAT('UI', UPPER(LEFT(UUID(), 7)));
    END IF;
END; //

DELIMITER ;
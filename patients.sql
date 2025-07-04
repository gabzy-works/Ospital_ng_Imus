CREATE TABLE patients (
    id INT PRIMARY KEY IDENTITY(1,1),
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    date_of_birth DATE,
    is_new_patient BIT NOT NULL, -- 1 for new, 0 for old
    created_at DATETIME DEFAULT GETDATE()
); 
steps = [
    (
        """
        CREATE TABLE certificates (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            info TEXT,
            date DATE NOT NULL,
            teacher_account_id INT REFERENCES accounts(id) ON DELETE CASCADE,
            course_id INT REFERENCES course(id) ON DELETE CASCADE,
            student_account_id INT REFERENCES accounts(id) ON DELETE CASCADE
        );
        """,
        """
        DROP TABLE certificates;
        """
    )
]

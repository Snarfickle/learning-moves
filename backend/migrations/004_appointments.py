steps = [
    (
        """
        CREATE TABLE appointments (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES accounts(id),
            instructor_id INT REFERENCES accounts(id),
            date DATE NOT NULL,
            time TIME NOT NULL,
            address VARCHAR(255) NOT NULL,
            city VARCHAR(100) NOT NULL,
            state VARCHAR(100) NOT NULL,
            zip VARCHAR(15) NOT NULL,
            country VARCHAR(100) NOT NULL
        );
        """,
        """
        DROP TABLE appointments;
        """
    )
]

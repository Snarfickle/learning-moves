steps = [
    (
        """
        CREATE TABLE materials (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            info TEXT,
            quantity INT NOT NULL,
            cost DECIMAL(10, 2) NOT NULL,
            free BOOLEAN NOT NULL,
            owner INT REFERENCES accounts(id) ON DELETE CASCADE
        );
        """,
        """
        DROP TABLE materials;
        """
    )
]

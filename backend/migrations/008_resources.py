steps = [
    (
        """
        CREATE TABLE resources (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            url_link TEXT NOT NULL,
            info TEXT,
            account_id INT REFERENCES accounts(id) ON DELETE CASCADE,
            date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        DROP TABLE resources;
        """
    )
]

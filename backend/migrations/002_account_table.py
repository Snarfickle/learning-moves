steps = [
    [
        # "Up" Table accounts SQL statement
        """
        CREATE TABLE accounts (
            id SERIAL PRIMARY KEY NOT NULL,
            username VARCHAR(1000) UNIQUE NOT NULL,
            email VARCHAR(1000) NOT NULL,
            password VARCHAR(2000) NOT NULL
        );
        """,
        # "Down" SQL Statement
        """
        DROP TABLE accounts;
        """,
    ],
]

steps = [
    [
        # "Up" SQL statement
        """
        ALTER TABLE profile 
        ADD COLUMN account_id INTEGER NOT NULL UNIQUE,
        ADD CONSTRAINT fk_profile_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(id);
        """,
        # "Down" SQL Statement
        """
        ALTER TABLE profile 
        DROP COLUMN account_id,
        DROP CONSTRAINT fk_profile_account;
        """,
    ],
]

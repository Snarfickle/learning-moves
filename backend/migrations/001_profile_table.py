steps = [
    [
        # "Up" Table profile SQL statement
        """
        CREATE TYPE profile_type AS ENUM ('student', 'teacher');
        CREATE TABLE profile (
            id SERIAL PRIMARY KEY NOT NULL,
            first_name  VARCHAR(1000) NULL,
            last_name VARCHAR(1000) NULL,
            email VARCHAR(1000) NULL,
            type profile_type NULL,
            phone_number VARCHAR(100) NULL,
            city VARCHAR(1000) NULL,
            state VARCHAR(1000) NULL,
            certificates VARCHAR(2000),
            profile_picture VARCHAR(1000),
            about_me VARCHAR(2000)
        );
        """,
        # DOWN SQL Statement
        """
        DROP TABLE profile;
        DROP TYPE profile_type;
        """,
    ],]

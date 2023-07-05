steps = [
    (
        """
        CREATE TABLE course (
            id SERIAL PRIMARY KEY,
            course_info TEXT,
            list_of_appointments TEXT,
            location BOOLEAN,
            date DATE NOT NULL,
            time TIME NOT NULL,
            address VARCHAR(255),
            city VARCHAR(100),
            state VARCHAR(100),
            zip VARCHAR(15),
            country VARCHAR(100),
            online BOOLEAN
        );
        """,
        """
        DROP TABLE course;
        """
    )
]
#list_of_appointments TEXT, -- This field is a placeholder; a more appropriate structure like a join table might be needed.

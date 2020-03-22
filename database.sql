CREATE TABLE users (
    username VARCHAR(50),
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (username)
);

CREATE TABLE student (
    student_number BIGINT,
    social_security_number VARCHAR(40),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    sex CHAR(1),
    current_address VARCHAR(100),
    current_phone_number VARCHAR(35),
    permanent_address VARCHAR(100),
    permanent_phone_number VARCHAR(35),
    class VARCHAR(50),
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (student_number)
);

CREATE TABLE permanent_address_detail (
    student_number BIGINT,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code INTEGER NOT NULL,
    PRIMARY KEY (student_number),
    FOREIGN KEY (student_number) REFERENCES student (student_number)
);

CREATE TABLE department (
    code BIGINT,
    name VARCHAR(100) NOT NULL,
    office_number SMALLINT,
    office_phone VARCHAR(35),
    college VARCHAR(50),
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (code)
);

CREATE TABLE student_department (
    student_number BIGINT,
    department_code BIGINT,
    from_start_date DATE NOT NULL,
    until_end_date DATE,
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (student_number, department_code),
    FOREIGN KEY (student_number) REFERENCES student (student_number),
    FOREIGN KEY (department_code) REFERENCES department (code)
);

CREATE TABLE course (
    course_number BIGINT,
    offering_department BIGINT,
    name VARCHAR(40) NOT NULL,
    description VARCHAR(70) NOT NULL,
    semester_hours INTEGER NOT NULL,
    course_level SMALLINT NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (course_number),
    FOREIGN KEY (offering_department) REFERENCES department (code)
);

CREATE TABLE student_course (
    student_number BIGINT,
    course_number BIGINT,
    PRIMARY KEY (student_number, course_number),
    FOREIGN KEY (student_number) REFERENCES student (student_number),
    FOREIGN KEY (course_number) REFERENCES course (course_number)
);

-- CREATE TABLE course_taken (
--     course_id BIGINT,
--     course_completed BOOLEAN DEFAULT TRUE,
--     grade_earned VARCHAR(40) NOT NULL,
--     credit_hours INTEGER NOT NULL,
--     course_level SMALLINT NOT NULL,
--     PRIMARY KEY (course_id)
-- );

-- CREATE TABLE degree (
--     degree_id BIGINT,
--     description VARCHAR(50) NOT NULL,
--     duration SMALLINT NOT NULL,
--     PRIMARY KEY (degree_id)
-- );

-- CREATE TABLE previos_college_info (
--     student_number BIGINT,
--     course_id BIGINT,
--     degree_id BIGINT,
--     college_name VARCHAR(50) NOT NULL,
--     start_date DATE NOT NULL,
--     end_date DATE,
--     PRIMARY KEY (student_number, course_id, degree_id),
--     FOREIGN KEY (student_number) REFERENCES student (student_number),
--     FOREIGN KEY (course_id) REFERENCES course_taken (course_id),
--     FOREIGN KEY (degree_id) REFERENCES degree (degree_id)
-- );

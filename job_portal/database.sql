
CREATE DATABASE IF NOT EXISTS job_portal;
USE job_portal;

DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS job_seekers;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id   INT PRIMARY KEY AUTO_INCREMENT,
    username  VARCHAR(50)  NOT NULL UNIQUE,
    password  VARCHAR(100) NOT NULL,
    user_type VARCHAR(20)  NOT NULL,
    CONSTRAINT chk_user_type CHECK (user_type IN ('Job Seeker', 'Company'))
);

CREATE TABLE job_seekers (
    seeker_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id   INT NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email     VARCHAR(100) NOT NULL,
    phone     VARCHAR(20)  NOT NULL,
    skills    VARCHAR(500) NOT NULL,
    CONSTRAINT fk_seekers_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE companies (
    company_id   INT PRIMARY KEY AUTO_INCREMENT,
    user_id      INT NOT NULL UNIQUE,
    company_name VARCHAR(100) NOT NULL,
    email        VARCHAR(100) NOT NULL,
    location     VARCHAR(100) NOT NULL,
    CONSTRAINT fk_companies_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE jobs (
    job_id          INT PRIMARY KEY AUTO_INCREMENT,
    company_id      INT NOT NULL,
    job_title       VARCHAR(100) NOT NULL,
    description     TEXT NOT NULL,
    location        VARCHAR(100) NOT NULL,
    salary          DECIMAL(10,2) NOT NULL,
    required_skills VARCHAR(500) NOT NULL,
    posted_date     DATE NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'Open',
    CONSTRAINT fk_jobs_company
        FOREIGN KEY (company_id) REFERENCES companies(company_id),
    CONSTRAINT chk_job_status CHECK (status IN ('Open', 'Closed'))
);

CREATE TABLE applications (
    application_id   INT PRIMARY KEY AUTO_INCREMENT,
    job_id           INT NOT NULL,
    seeker_id        INT NOT NULL,
    application_date DATE NOT NULL,
    status           VARCHAR(20) NOT NULL DEFAULT 'Applied',
    CONSTRAINT fk_applications_job
        FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    CONSTRAINT fk_applications_seeker
        FOREIGN KEY (seeker_id) REFERENCES job_seekers(seeker_id),
    CONSTRAINT uq_job_seeker UNIQUE (job_id, seeker_id),
    CONSTRAINT chk_app_status CHECK (status IN ('Applied', 'Selected', 'Rejected'))
);

INSERT INTO users (username, password, user_type) VALUES
    ('rahul',      '1234',   'Job Seeker'),
    ('anu',        'pass1',  'Job Seeker'),
    ('meera',      'pass2',  'Job Seeker'),
    ('techcorp',   'abc123', 'Company'),
    ('abctech',    'abc123', 'Company'),
    ('datacorp',   'abc123', 'Company');

INSERT INTO job_seekers (user_id, full_name, email, phone, skills) VALUES
    (1, 'Rahul Kumar',    'rahul@gmail.com', '9876543210', 'Python, MySQL, Java'),
    (2, 'Anu Joseph',     'anu@gmail.com',   '9876500001', 'HTML, CSS, JavaScript, Python'),
    (3, 'Meera Thomas',   'meera@gmail.com', '9876500002', 'Excel, SQL, Data Analysis');

INSERT INTO companies (user_id, company_name, email, location) VALUES
    (4, 'Tech Solutions',    'hr@techsolutions.com', 'Kochi'),
    (5, 'ABC Technologies',  'jobs@abctech.com',     'Bangalore'),
    (6, 'Data Corp',         'careers@datacorp.com', 'Chennai');

ALTER TABLE jobs AUTO_INCREMENT = 101;

INSERT INTO jobs (company_id, job_title, description, location, salary, required_skills, posted_date, status) VALUES
    (1, 'Python Developer',
        'Looking for a beginner Python developer with basic MySQL knowledge.',
        'Kochi', 30000.00, 'Python, MySQL', '2026-08-01', 'Open'),
    (1, 'Python Intern',
        'Internship for students who know Python basics.',
        'Kochi', 12000.00, 'Python', '2026-08-10', 'Open'),
    (1, 'Backend Developer',
        'Work on REST-style backend logic using Python.',
        'Kochi', 40000.00, 'Python, MySQL, APIs', '2026-07-20', 'Closed'),
    (2, 'Web Developer',
        'Build simple websites using HTML, CSS and JavaScript.',
        'Bangalore', 35000.00, 'HTML, CSS, JavaScript', '2026-08-05', 'Open'),
    (2, 'Java Developer',
        'Entry-level Java developer for desktop and backend tasks.',
        'Bangalore', 38000.00, 'Java, MySQL', '2026-08-12', 'Open'),
    (3, 'Data Analyst',
        'Analyze datasets and prepare reports using SQL and Excel.',
        'Chennai', 32000.00, 'SQL, Excel, Data Analysis', '2026-08-03', 'Open'),
    (3, 'SQL Developer',
        'Write queries, joins and reports for business teams.',
        'Chennai', 34000.00, 'SQL, MySQL', '2026-08-15', 'Open'),
    (2, 'Python Developer',
        'Second Python role at ABC Technologies for web scripting.',
        'Bangalore', 36000.00, 'Python, JavaScript', '2026-08-18', 'Open'),
    (3, 'Junior Tester',
        'Manual testing of web applications. Closed for new applications.',
        'Chennai', 25000.00, 'Testing, SQL', '2026-06-01', 'Closed');

INSERT INTO applications (job_id, seeker_id, application_date, status) VALUES
    (101, 1, '2026-08-20', 'Applied'),
    (106, 1, '2026-08-21', 'Selected'),
    (104, 1, '2026-08-22', 'Rejected'),
    (101, 2, '2026-08-21', 'Applied'),
    (104, 2, '2026-08-23', 'Applied'),
    (106, 3, '2026-08-24', 'Selected');

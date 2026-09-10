"""
********** MySQL COMMANDS **********

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

"""


import mysql.connector
from mysql.connector import Error
from datetime import date

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "rosalynee",
    "database": "job_portal",
}

def connect_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as err:
        print("Database error:", err)
        print("Check host, username, password, and that the job_portal database exists.")
        return None

def get_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Try again.")

def pause():
    input("\nPress Enter to continue...")

def print_header(title):
    print("\n******************************")
    print(title.center(40))
    print("******************************")

def username_exists(connection, username):
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    return row is not None

def register_job_seeker(connection):
    print_header("JOB SEEKER REGISTRATION")
    full_name = get_nonempty("Full name: ")
    email = get_nonempty("Email: ")
    phone = get_nonempty("Phone: ")
    skills = get_nonempty("Skills: ")
    username = get_nonempty("Username: ")
    password = get_nonempty("Password: ")
    if username_exists(connection, username):
        print("That username is already taken. Choose another one.")
        return
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)",
            (username, password, "Job Seeker"),
        )
        user_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO job_seekers (user_id, full_name, email, phone, skills)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, full_name, email, phone, skills),
        )
        connection.commit()
        cursor.close()
        print("\nRegistration successful!")
        print("You can now log in with username:", username)
    except Error as err:
        connection.rollback()
        print("Database error:", err)

def register_company(connection):
    print_header("COMPANY REGISTRATION")
    company_name = get_nonempty("Company name: ")
    email = get_nonempty("Email: ")
    location = get_nonempty("Location: ")
    username = get_nonempty("Username: ")
    password = get_nonempty("Password: ")
    if username_exists(connection, username):
        print("That username is already taken. Choose another one.")
        return
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)",
            (username, password, "Company"),
        )
        user_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO companies (user_id, company_name, email, location)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, company_name, email, location),
        )
        connection.commit()
        cursor.close()
        print("\nRegistration successful!")
        print("You can now log in with username:", username)
    except Error as err:
        connection.rollback()
        print("Database error:", err)

def register_user(connection):
    print("\n********** ACCOUNT TYPE **********\n")
    print("1. Job Seeker")
    print("2. Company")
    choice = input("\nEnter your choice: ").strip()
    if choice == "1":
        register_job_seeker(connection)
    elif choice == "2":
        register_company(connection)
    else:
        print("Invalid choice. Registration cancelled.")

def login_user(connection):
    print_header("LOGIN")
    username = get_nonempty("Username: ")
    password = get_nonempty("Password: ")
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT user_id, username, user_type
            FROM users
            WHERE username = %s AND password = %s
            """,
            (username, password),
        )
        user = cursor.fetchone()
        if user is None:
            cursor.close()
            print("Invalid username or password.")
            return None
        if user["user_type"] == "Job Seeker":
            cursor.execute(
                "SELECT seeker_id, full_name FROM job_seekers WHERE user_id = %s",
                (user["user_id"],),
            )
            profile = cursor.fetchone()
            if profile is None:
                cursor.close()
                print("Job seeker profile is missing for this account.")
                return None
            user["seeker_id"] = profile["seeker_id"]
            user["full_name"] = profile["full_name"]
        else:
            cursor.execute(
                "SELECT company_id, company_name FROM companies WHERE user_id = %s",
                (user["user_id"],),
            )
            profile = cursor.fetchone()
            if profile is None:
                cursor.close()
                print("Company profile is missing for this account.")
                return None
            user["company_id"] = profile["company_id"]
            user["company_name"] = profile["company_name"]
        cursor.close()
        print("\nLogin successful! Welcome,", user["username"])
        return user
    except Error as err:
        print("Database error:", err)
        return None

def logout():
    """Clear the idea of a logged-in user (caller sets current_user to None)."""
    print("Logged out successfully.")

def view_all_jobs(connection):
    print("\n********** AVAILABLE JOBS **********\n")
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT j.job_id, j.job_title, c.company_name, j.location
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE j.status = 'Open'
            ORDER BY j.job_id
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            print("No open jobs right now.")
            return
        print(f"{'ID':<7}{'Job Title':<22}{'Company':<22}{'Location'}")
        print("-" * 70)
        for job_id, title, company, location in rows:
            print(f"{job_id:<7}{title[:20]:<22}{company[:20]:<22}{location}")
    except Error as err:
        print("Database error:", err)

def search_jobs(connection):
    
    print("\n********** SEARCH JOBS **********\n")
    keyword = get_nonempty("Enter job title, location, or skill keyword: ")
    pattern = "%" + keyword + "%"
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT j.job_id, j.job_title, c.company_name, j.location
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE j.status = 'Open'
              AND (j.job_title LIKE %s
                   OR j.location LIKE %s
                   OR j.required_skills LIKE %s)
            ORDER BY j.job_id
            """,
            (pattern, pattern, pattern),
        )
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            print("No matching open jobs found.")
            return
        print(f"\n{'ID':<7}{'Job Title':<22}{'Company':<22}{'Location'}")
        print("-" * 65)
        for job_id, title, company, location in rows:
            print(f"{job_id:<7}{title[:20]:<22}{company[:20]:<22}{location}")
    except Error as err:
        print("Database error:", err)

def view_job_details(connection):
    print_header("JOB DETAILS")
    job_id_text = get_nonempty("Enter Job ID: ")
    if not job_id_text.isdigit():
        print("Job ID must be a number.")
        return
    job_id = int(job_id_text)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT j.job_id, j.job_title, c.company_name, j.location,
                   j.salary, j.required_skills, j.description, j.status
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE j.job_id = %s
            """,
            (job_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            print("No job found with that ID.")
            return
        job_id, title, company, location, salary, skills, description, status = row
        print(f"\nJob ID: {job_id}")
        print(f"Job Title: {title}")
        print(f"Company: {company}")
        print(f"Location: {location}")
        print(f"Salary: Rs.{salary:,.2f}")
        print(f"\nRequired Skills:\n{skills}")
        print(f"\nDescription:\n{description}")
        print(f"\nStatus: {status}")
        print("******************************")
    except Error as err:
        print("Database error:", err)

def apply_for_job(connection, seeker_id):
    print_header("APPLY FOR A JOB")
    job_id_text = get_nonempty("Enter Job ID to apply: ")
    if not job_id_text.isdigit():
        print("Job ID must be a number.")
        return
    job_id = int(job_id_text)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT j.job_id, j.job_title, j.status, c.company_name
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE j.job_id = %s
            """,
            (job_id,),
        )
        job = cursor.fetchone()
        if job is None:
            cursor.close()
            print("That job does not exist.")
            return
        _job_id, title, status, company = job
        if status != "Open":
            cursor.close()
            print("This job is no longer accepting applications.")
            return
        cursor.execute(
            "SELECT application_id FROM applications WHERE job_id = %s AND seeker_id = %s",
            (job_id, seeker_id),
        )
        existing = cursor.fetchone()
        if existing is not None:
            cursor.close()
            print("You have already applied for this job.")
            return
        cursor.execute(
            """
            INSERT INTO applications (job_id, seeker_id, application_date, status)
            VALUES (%s, %s, %s, %s)
            """,
            (job_id, seeker_id, date.today(), "Applied"),
        )
        application_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        print("\nApplication submitted successfully!")
        print(f"Application ID: {application_id}")
        print(f"Job: {title}")
        print(f"Company: {company}")
    except Error as err:
        connection.rollback()
        print("Database error:", err)

def view_my_applications(connection, seeker_id):
    print("\n********** MY APPLICATIONS **********\n")
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT a.application_id, j.job_title, c.company_name,
                   a.application_date, a.status
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
            WHERE a.seeker_id = %s
            ORDER BY a.application_id
            """,
            (seeker_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            print("You have not applied for any jobs yet.")
            return
        print(f"{'Application ID':<17}{'Job':<22}{'Company':<20}{'Date':<14}{'Status'}")
        print("-" * 85)
        for app_id, title, company, app_date, status in rows:
            print(f"{app_id:<17}{title[:20]:<22}{company[:18]:<20}{str(app_date):<14}{status}")
    except Error as err:
        print("Database error:", err)

def job_seeker_dashboard(connection, user):
    while True:
        print_header("JOB SEEKER DASHBOARD")
        print("1. View All Jobs")
        print("2. Search Jobs")
        print("3. View Job Details")
        print("4. Apply for a Job")
        print("5. My Applications")
        print("6. Logout")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            view_all_jobs(connection)
            pause()
        elif choice == "2":
            search_jobs(connection)
            pause()
        elif choice == "3":
            view_job_details(connection)
            pause()
        elif choice == "4":
            apply_for_job(connection, user["seeker_id"])
            pause()
        elif choice == "5":
            view_my_applications(connection, user["seeker_id"])
            pause()
        elif choice == "6":
            logout()
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")

def post_job(connection, company_id):
    print("\n********** POST A JOB **********\n")
    job_title = get_nonempty("Job title: ")
    description = get_nonempty("Description: ")
    location = get_nonempty("Location: ")
    while True:
        salary_text = get_nonempty("Salary: ")
        try:
            salary = float(salary_text)
            if salary <= 0:
                print("Salary must be greater than 0.")
                continue
            break
        except ValueError:
            print("Salary must be a number. Example: 30000")
    required_skills = get_nonempty("Required skills: ")
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO jobs
                (company_id, job_title, description, location, salary,
                 required_skills, posted_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                company_id,
                job_title,
                description,
                location,
                salary,
                required_skills,
                date.today(),
                "Open",
            ),
        )
        job_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        print("\nJob posted successfully!")
        print("Job ID:", job_id)
    except Error as err:
        connection.rollback()
        print("Database error:", err)

def view_my_jobs(connection, company_id):
    print("\n********** MY JOBS **********\n")
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT job_id, job_title, location, status
            FROM jobs
            WHERE company_id = %s
            ORDER BY job_id
            """,
            (company_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            print("You have not posted any jobs yet.")
            return
        print(f"{'ID':<7}{'Job Title':<22}{'Location':<16}{'Status'}")
        print("-" * 55)
        for job_id, title, location, status in rows:
            print(f"{job_id:<7}{title[:20]:<22}{location[:14]:<16}{status}")
    except Error as err:
        print("Database error:", err)

def view_applications(connection, company_id):
    print("\n********** APPLICATIONS **********\n")
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT j.job_title, a.application_id, js.full_name, js.email, a.status
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            JOIN job_seekers js ON a.seeker_id = js.seeker_id
            WHERE j.company_id = %s
            ORDER BY j.job_id, a.application_id
            """,
            (company_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            print("No applications for your jobs yet.")
            return
        current_job = None
        for job_title, app_id, name, email, status in rows:
            if job_title != current_job:
                current_job = job_title
                print(f"\nJob: {job_title}")
                print(f"{'Application ID':<17}{'Applicant':<18}{'Email':<24}{'Status'}")
                print("-" * 70)
            print(f"{app_id:<17}{name[:16]:<18}{email[:22]:<24}{status}")
    except Error as err:
        print("Database error:", err)

def update_application_status(connection, company_id):
    print_header("UPDATE APPLICATION STATUS")
    app_id_text = get_nonempty("Enter Application ID: ")
    if not app_id_text.isdigit():
        print("Application ID must be a number.")
        return
    application_id = int(app_id_text)
    print("\n1. Selected")
    print("2. Rejected")
    print("3. Applied")
    choice = input("\nEnter choice: ").strip()
    status_map = {"1": "Selected", "2": "Rejected", "3": "Applied"}
    if choice not in status_map:
        print("Invalid choice.")
        return
    new_status = status_map[choice]
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT a.application_id
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE a.application_id = %s AND j.company_id = %s
            """,
            (application_id, company_id),
        )
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            print("Application not found, or it does not belong to your company.")
            return
        cursor.execute(
            "UPDATE applications SET status = %s WHERE application_id = %s",
            (new_status, application_id),
        )
        connection.commit()
        cursor.close()
        print("\nApplication status updated successfully!")
    except Error as err:
        connection.rollback()
        print("Database error:", err)

def close_job(connection, company_id):
    print_header("CLOSE A JOB")
    job_id_text = get_nonempty("Enter Job ID to close: ")
    if not job_id_text.isdigit():
        print("Job ID must be a number.")
        return
    job_id = int(job_id_text)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT job_id, status FROM jobs WHERE job_id = %s AND company_id = %s",
            (job_id, company_id),
        )
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            print("Job not found, or it does not belong to your company.")
            return
        if row[1] == "Closed":
            cursor.close()
            print("This job is already closed.")
            return
        cursor.execute(
            "UPDATE jobs SET status = 'Closed' WHERE job_id = %s AND company_id = %s",
            (job_id, company_id),
        )
        connection.commit()
        cursor.close()
        print("Job closed successfully.")
    except Error as err:
        connection.rollback()
        print("Database error:", err)

def company_dashboard(connection, user):
    while True:
        print_header("COMPANY DASHBOARD")
        print("1. Post a Job")
        print("2. View My Jobs")
        print("3. View Applications")
        print("4. Update Application Status")
        print("5. Close a Job")
        print("6. Logout")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            post_job(connection, user["company_id"])
            pause()
        elif choice == "2":
            view_my_jobs(connection, user["company_id"])
            pause()
        elif choice == "3":
            view_applications(connection, user["company_id"])
            pause()
        elif choice == "4":
            update_application_status(connection, user["company_id"])
            pause()
        elif choice == "5":
            close_job(connection, user["company_id"])
            pause()
        elif choice == "6":
            logout()
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")

def main():
    connection = connect_database()
    if connection is None:
        return
    try:
        while True:
            print_header("JOB PORTAL SYSTEM")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("\nEnter your choice: ").strip()
            if choice == "1":
                register_user(connection)
                pause()
            elif choice == "2":
                user = login_user(connection)
                if user is None:
                    pause()
                elif user["user_type"] == "Job Seeker":
                    job_seeker_dashboard(connection, user)
                elif user["user_type"] == "Company":
                    company_dashboard(connection, user)
                else:
                    print("Unknown account type.")
            elif choice == "3":
                print("Thank you for using Job Portal System.")
                break
            else:
                print("Invalid choice. Enter 1, 2, or 3.")
    finally:
        connection.close()

if __name__ == "__main__":
    main()

"""
STUDENT ATTENDANCE MANAGEMENT SYSTEM

Features:
1. Add Student
2. View Students
3. Mark Attendance
4. View Attendance
5. Calculate Attendance Percentage
6. Exit
"""



"""
***BEFORE RUNNING THIS PYTHON PROGRAM, CREATE THE FOLLOWING TABLES IN MySQL***

CREATE DATABASE student_attendance;

USE student_attendance;

CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL
);

CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    UNIQUE KEY unique_attendance (student_id, date)
);

"""


import mysql.connector
from mysql.connector import Error


# Connecting to MySQL Database

def create_connection():
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="rosalynee",         
            database="student_attendance"
        )
        return connection
    except Error as e:
        print(f"\n[Database Error] Could not connect to MySQL: {e}")
        return None


# Adding Student

def add_student(connection):
    print("\n\t Add Student \t")

    student_id = input("Enter student ID: ").strip()
    name = input("Enter student name: ").strip()
    department = input("Enter department: ").strip()

    if not student_id or not name or not department:
        print("All fields are required. Student not added.")
        return
    if not student_id.isdigit():
        print("Student ID must be a number.")
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO students (id, name, department) VALUES (%s, %s, %s)"
        cursor.execute(query, (int(student_id), name, department))
        connection.commit()
        print("\nStudent added successfully!")
    except mysql.connector.IntegrityError:
        # This error occurs when the same primary key (id) is inserted again
        print(f"\nStudent ID {student_id} already exists. Please use a different ID.")
    except Error as e:
        print(f"\n[Database Error] {e}")
    finally:
        cursor.close()


# View Students

def view_students(connection):
    print("\n\t Student List \t")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, name, department FROM students ORDER BY id")
        students = cursor.fetchall()

        if not students:
            print("No students found.")
            return
        print(f"{'ID':<8}{'Name':<20}{'Department':<20}")
        print("-" * 48)
        for student in students:
            student_id, name, department = student
            print(f"{student_id:<8}{name:<20}{department:<20}")

    except Error as e:
        print(f"\n[Database Error] {e}")
    finally:
        cursor.close()


# Check if a student exists

def get_student(connection, student_id):
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, department FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    return student


# Mark Attendance

def mark_attendance(connection):
    print("\n\t Mark Attendance \t")
    student_id = input("Enter student ID: ").strip()
    if not student_id.isdigit():
        print("Student ID must be a number.")
        return
    student = get_student(connection, int(student_id))
    if not student:
        print(f"No student found with ID {student_id}.")
        return
    _, name, department = student
    print(f"\nStudent: {name}")
    print(f"Department: {department}")

    date = input("Enter date (YYYY-MM-DD): ").strip()
    if not date:
        print("Date cannot be empty.")
        return
    print("\n1. Present")
    print("2. Absent")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        status = "Present"
    elif choice == "2":
        status = "Absent"
    else:
        print("Invalid choice. Attendance not marked.")
        return
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO attendance (student_id, date, status)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (int(student_id), date, status))
        connection.commit()
        print("\nAttendance marked successfully!")
    except mysql.connector.IntegrityError:
        # This happens because of the UNIQUE constraint on (student_id, date)
        print(f"\nAttendance for student {student_id} on {date} is already marked.")
    except Error as e:
        print(f"\n[Database Error] {e}")
    finally:
        cursor.close()


# View Attendance

def view_attendance(connection):
    print("\n\t View Attendance \t")
    student_id = input("Enter student ID: ").strip()
    if not student_id.isdigit():
        print("Student ID must be a number.")
        return
    student = get_student(connection, int(student_id))
    if not student:
        print(f"No student found with ID {student_id}.")
        return
    _, name, _ = student
    print(f"\nAttendance for {name}\n")

    cursor = connection.cursor()
    try:
        query = """
            SELECT date, status FROM attendance
            WHERE student_id = %s
            ORDER BY date
        """
        cursor.execute(query, (int(student_id),))
        records = cursor.fetchall()
        if not records:
            print("No attendance records found for this student.")
            return
        print(f"{'Date':<15}{'Status':<10}")
        print("-" * 25)
        for date, status in records:
            print(f"{str(date):<15}{status:<10}")

    except Error as e:
        print(f"\n[Database Error] {e}")
    finally:
        cursor.close()


# Calculateing The Attendance Percentage

def calculate_percentage(connection):
    print("\n\t Attendance Percentage \t")
    student_id = input("Enter student ID: ").strip()
    if not student_id.isdigit():
        print("Student ID must be a number.")
        return
    student = get_student(connection, int(student_id))
    if not student:
        print(f"No student found with ID {student_id}.")
        return
    _, name, _ = student

    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id = %s",
            (int(student_id),)
        )
        total = cursor.fetchone()[0]
        if total == 0:
            print(f"\nStudent: {name}")
            print("No attendance records found. Percentage cannot be calculated.")
            return
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id = %s AND status = 'Present'",
            (int(student_id),)
        )
        present = cursor.fetchone()[0]
        absent = total - present
        percentage = (present / total) * 100
        print(f"\nStudent: {name}")
        print(f"Total Classes: {total}")
        print(f"Present: {present}")
        print(f"Absent: {absent}")
        print(f"Attendance Percentage: {percentage:.0f}%")

    except Error as e:
        print(f"\n[Database Error] {e}")
    finally:
        cursor.close()


# MAIN MENU

def main():
    connection = create_connection()
    if connection is None:
        print("Exiting program because the database connection failed.")
        return

    while True:
        print("\n================================")
        print("     STUDENT ATTENDANCE SYSTEM")
        print("================================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Mark Attendance")
        print("4. View Attendance")
        print("5. Calculate Attendance Percentage")
        print("6. Exit")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            add_student(connection)
        elif choice == "2":
            view_students(connection)
        elif choice == "3":
            mark_attendance(connection)
        elif choice == "4":
            view_attendance(connection)
        elif choice == "5":
            calculate_percentage(connection)
        elif choice == "6":
            print("\nExiting the program. Goodbye!")
            connection.close()
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")



main()

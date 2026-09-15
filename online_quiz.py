"""
********** MySQL COMMANDS **********

DROP DATABASE IF EXISTS online_quiz;
CREATE DATABASE online_quiz;
USE online_quiz;

CREATE TABLE Users (
    user_id     INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(100) NOT NULL,
    full_name   VARCHAR(100) NOT NULL
);

CREATE TABLE Categories (
    category_id     INT AUTO_INCREMENT PRIMARY KEY,
    category_name   VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Questions (
    question_id     INT AUTO_INCREMENT PRIMARY KEY,
    category_id     INT NOT NULL,
    question_text   VARCHAR(500) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        ON DELETE CASCADE
);

CREATE TABLE Options (
    option_id       INT AUTO_INCREMENT PRIMARY KEY,
    question_id     INT NOT NULL,
    option_text     VARCHAR(255) NOT NULL,
    is_correct      BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
        ON DELETE CASCADE
);

CREATE TABLE Quiz_Attempts (
    attempt_id      INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    category_id     INT NOT NULL,
    attempt_date    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        ON DELETE CASCADE
);

CREATE TABLE Results (
    result_id           INT AUTO_INCREMENT PRIMARY KEY,
    attempt_id          INT NOT NULL,
    total_questions      INT NOT NULL,
    correct_answers       INT NOT NULL,
    wrong_answers         INT NOT NULL,
    score                 INT NOT NULL,
    percentage            DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (attempt_id) REFERENCES Quiz_Attempts(attempt_id)
        ON DELETE CASCADE
);

INSERT INTO Categories (category_name) VALUES
('Python'),
('MySQL'),
('General Knowledge'),
('Mathematics');

INSERT INTO Questions (category_id, question_text) VALUES
(1, 'Which keyword is used to define a function in Python?'),
(1, 'Which function is used to display output in Python?'),
(1, 'Which symbol is used to start a comment in Python?'),
(1, 'Which data type is used to store True or False values in Python?'),
(1, 'Which list method adds an element to the end of a list?'),
(1, 'Which keyword creates a loop that repeats while a condition is true?');

INSERT INTO Options (question_id, option_text, is_correct) VALUES
(1, 'function', FALSE),
(1, 'def', TRUE),
(1, 'define', FALSE),
(1, 'func', FALSE),

(2, 'print()', TRUE),
(2, 'display()', FALSE),
(2, 'echo()', FALSE),
(2, 'show()', FALSE),

(3, '//', FALSE),
(3, '#', TRUE),
(3, '--', FALSE),
(3, '/*', FALSE),

(4, 'bool', TRUE),
(4, 'boolean', FALSE),
(4, 'bit', FALSE),
(4, 'flag', FALSE),

(5, 'add()', FALSE),
(5, 'append()', TRUE),
(5, 'insert()', FALSE),
(5, 'push()', FALSE),

(6, 'for', FALSE),
(6, 'while', TRUE),
(6, 'loop', FALSE),
(6, 'repeat', FALSE);

INSERT INTO Questions (category_id, question_text) VALUES
(2, 'Which command is used to retrieve data from a table?'),
(2, 'Which command is used to add new data into a table?'),
(2, 'Which command is used to remove a table completely from a database?'),
(2, 'Which clause is used to filter rows in SQL?'),
(2, 'Which keyword is used to sort the result set in SQL?'),
(2, 'Which keyword is used to combine rows from two or more tables?');

INSERT INTO Options (question_id, option_text, is_correct) VALUES
(7, 'SELECT', TRUE),
(7, 'UPDATE', FALSE),
(7, 'DELETE', FALSE),
(7, 'CREATE', FALSE),

(8, 'ADD', FALSE),
(8, 'INSERT', TRUE),
(8, 'PUT', FALSE),
(8, 'NEW', FALSE),

(9, 'DELETE TABLE', FALSE),
(9, 'DROP TABLE', TRUE),
(9, 'REMOVE TABLE', FALSE),
(9, 'CLEAR TABLE', FALSE),

(10, 'WHERE', TRUE),
(10, 'HAVING', FALSE),
(10, 'FILTER', FALSE),
(10, 'GROUP BY', FALSE),

(11, 'SORT BY', FALSE),
(11, 'ORDER BY', TRUE),
(11, 'ARRANGE BY', FALSE),
(11, 'GROUP BY', FALSE),

(12, 'JOIN', TRUE),
(12, 'MERGE', FALSE),
(12, 'LINK', FALSE),
(12, 'COMBINE', FALSE);

INSERT INTO Questions (category_id, question_text) VALUES
(3, 'Which planet is known as the Red Planet?'),
(3, 'What is the capital of India?'),
(3, 'Who wrote the play Romeo and Juliet?'),
(3, 'Which is the largest ocean on Earth?'),
(3, 'How many continents are there on Earth?'),
(3, 'Which gas do plants absorb from the atmosphere for photosynthesis?');

INSERT INTO Options (question_id, option_text, is_correct) VALUES
(13, 'Earth', FALSE),
(13, 'Mars', TRUE),
(13, 'Jupiter', FALSE),
(13, 'Venus', FALSE),

(14, 'Mumbai', FALSE),
(14, 'Chennai', FALSE),
(14, 'New Delhi', TRUE),
(14, 'Kolkata', FALSE),

(15, 'Charles Dickens', FALSE),
(15, 'William Shakespeare', TRUE),
(15, 'Mark Twain', FALSE),
(15, 'Leo Tolstoy', FALSE),

(16, 'Atlantic Ocean', FALSE),
(16, 'Indian Ocean', FALSE),
(16, 'Pacific Ocean', TRUE),
(16, 'Arctic Ocean', FALSE),

(17, '5', FALSE),
(17, '6', FALSE),
(17, '7', TRUE),
(17, '8', FALSE),

(18, 'Oxygen', FALSE),
(18, 'Nitrogen', FALSE),
(18, 'Carbon Dioxide', TRUE),
(18, 'Hydrogen', FALSE);

INSERT INTO Questions (category_id, question_text) VALUES
(4, 'What is the value of 7 x 8?'),
(4, 'What is the square root of 144?'),
(4, 'What is the value of Pi rounded to two decimal places?'),
(4, 'What is 15% of 200?'),
(4, 'How many sides does a hexagon have?'),
(4, 'What is the sum of interior angles in a triangle?');

INSERT INTO Options (question_id, option_text, is_correct) VALUES
(19, '54', FALSE),
(19, '56', TRUE),
(19, '58', FALSE),
(19, '64', FALSE),

(20, '10', FALSE),
(20, '11', FALSE),
(20, '12', TRUE),
(20, '14', FALSE),

(21, '3.12', FALSE),
(21, '3.14', TRUE),
(21, '3.16', FALSE),
(21, '3.41', FALSE),

(22, '20', FALSE),
(22, '25', FALSE),
(22, '30', TRUE),
(22, '35', FALSE),

(23, '5', FALSE),
(23, '6', TRUE),
(23, '7', FALSE),
(23, '8', FALSE),

(24, '90 degrees', FALSE),
(24, '180 degrees', TRUE),
(24, '270 degrees', FALSE),
(24, '360 degrees', FALSE);

"""



import random
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "rosalynee",
    "database": "online_quiz",
}

def connect_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None

def register_user(connection):
    print("\n********** REGISTRATION **********")
    full_name = input("Enter full name: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    if not full_name or not username or not password:
        print("\nAll fields are required. Registration cancelled.")
        return
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("\nUsername already exists.")
            print("Please choose another username.")
            return
        cursor.execute("INSERT INTO Users (username, password, full_name) VALUES (%s, %s, %s)",
            (username, password, full_name),
        )
        connection.commit()
        print("\nRegistration successful!")
        print("You can now login.")
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"\nError while registering: {err}")
    finally:
        cursor.close()

def login_user(connection):
    print("\n********** LOGIN **********")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT user_id, username, full_name FROM Users "
            "WHERE username = %s AND password = %s",
            (username, password),
            )
        user = cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"\nError while logging in: {err}")
        return None
    finally:
        cursor.close()
    if user:
        print("\nLogin successful!")
        print(f"\nWelcome, {user['full_name']}!")
        return user
    print("\nInvalid username or password.")
    return None

def show_categories(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT category_id, category_name FROM Categories ORDER BY category_id")
        categories = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"\nError fetching categories: {err}")
        return []
    finally:
        cursor.close()
    print("\n********** QUIZ CATEGORIES **********\n")
    for cat_id, cat_name in categories:
        print(f"{cat_id}. {cat_name}")
    return categories


def get_random_questions(connection, category_id, limit=5):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT question_id, question_text FROM Questions "
            "WHERE category_id = %s ORDER BY RAND() LIMIT %s",
            (category_id, limit),
        )
        questions = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"\nError fetching questions: {err}")
        questions = []
    finally:
        cursor.close()
    return questions

def get_question_options(connection, question_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT option_id, option_text, is_correct FROM Options WHERE question_id = %s",
            (question_id,),
        )
        options = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"\nError fetching options: {err}")
        options = []
    finally:
        cursor.close()
    random.shuffle(options)
    return options

def check_answer(selected_option):
    return bool(selected_option["is_correct"])

def calculate_score(correct_answers, total_questions):
    score = correct_answers
    percentage = round((correct_answers / total_questions) * 100, 2)
    return score, percentage

def save_result(connection, user_id, category_id, total_questions,correct_answers, wrong_answers, score, percentage):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Quiz_Attempts (user_id, category_id) VALUES (%s, %s)",
            (user_id, category_id),
        )
        attempt_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO Results "
            "(attempt_id, total_questions, correct_answers, wrong_answers, score, percentage) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (attempt_id, total_questions, correct_answers, wrong_answers, score, percentage),
        )
        connection.commit()
        return attempt_id
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"\nError while saving result: {err}")
        return None
    finally:
        cursor.close()

def start_quiz(connection, user):
    categories = show_categories(connection)
    if not categories:
        print("\nNo categories available right now.")
        return
    choice = input("\nEnter category: ").strip()
    if not choice.isdigit():
        print("\nInvalid category selection.")
        return
    category_id = int(choice)
    category_map = dict(categories)
    if category_id not in category_map:
        print("\nInvalid category selection.")
        return
    category_name = category_map[category_id]
    questions = get_random_questions(connection, category_id, 5)
    if len(questions) < 5:
        print(f"\nNot enough questions available in '{category_name}' to start a quiz "
              f"(need 5, found {len(questions)}).")
        return
    print(f"\nStarting {category_name} Quiz...\n")
    correct_answers = 0
    total_questions = len(questions)
    letters = ["A", "B", "C", "D"]

    for index, question in enumerate(questions, start=1):
        print("=" * 40)
        print(f"Question {index} of {total_questions}")
        print("=" * 40)
        print(f"\n{question['question_text']}\n")
        options = get_question_options(connection, question["question_id"])
        if not options:
            print("This question has no options configured. Skipping.\n")
            continue
        valid_letters = letters[: len(options)]
        for letter, option in zip(valid_letters, options):
            print(f"{letter}. {option['option_text']}")
        answer = input("\nEnter your answer: ").strip().upper()
        selected = None
        if answer in valid_letters:
            selected = options[valid_letters.index(answer)]
        else:
            print("\nInvalid answer choice.")
        correct_option = next(opt for opt in options if opt["is_correct"])
        if selected and check_answer(selected):
            print("\nCorrect!\n")
            correct_answers += 1
        else:
            correct_letter = valid_letters[options.index(correct_option)]
            print("\nWrong!")
            print(f"Correct answer: {correct_letter}. {correct_option['option_text']}\n")
    wrong_answers = total_questions - correct_answers
    score, percentage = calculate_score(correct_answers, total_questions)
    print("=" * 40)
    print("********** QUIZ RESULT **********")
    print("=" * 40)
    print(f"\nCategory: {category_name}\n")
    print(f"Total Questions: {total_questions}")
    print(f"Correct Answers: {correct_answers}")
    print(f"Wrong Answers: {wrong_answers}\n")
    print(f"Score: {score}/{total_questions}")
    print(f"Percentage: {percentage}%")
    print("=" * 40)
    attempt_id = save_result(
        connection, user["user_id"], category_id,
        total_questions, correct_answers, wrong_answers, score, percentage,
    )
    if attempt_id:
        print("\nResult saved successfully!")
        print(f"Attempt ID: {attempt_id}")

def show_previous_results(connection, user):
    """Show every past attempt for the logged-in user via a JOIN across 3 tables."""
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT qa.attempt_id, c.category_name, r.score, r.total_questions, r.percentage
            FROM Quiz_Attempts qa
            JOIN Categories c ON qa.category_id = c.category_id
            JOIN Results r ON qa.attempt_id = r.attempt_id
            WHERE qa.user_id = %s
            ORDER BY qa.attempt_id
            """,
            (user["user_id"],),
        )
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"\nError fetching previous results: {err}")
        return
    finally:
        cursor.close()
    print("\n********** PREVIOUS RESULTS **********\n")
    if not rows:
        print("You haven't attempted any quiz yet.")
        return
    print(f"{'Attempt ID':<12}{'Category':<20}{'Score':<10}{'Percentage'}")
    print("-" * 55)
    for row in rows:
        score_str = f"{row['score']}/{row['total_questions']}"
        print(f"{row['attempt_id']:<12}{row['category_name']:<20}{score_str:<10}{row['percentage']}%")

def show_leaderboard(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT u.full_name, c.category_name, r.score, r.total_questions
            FROM Results r
            JOIN Quiz_Attempts qa ON r.attempt_id = qa.attempt_id
            JOIN Users u ON qa.user_id = u.user_id
            JOIN Categories c ON qa.category_id = c.category_id
            ORDER BY r.score DESC, r.percentage DESC
            LIMIT 10
            """
        )
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"\nError fetching leaderboard: {err}")
        return
    finally:
        cursor.close()
    print("\n" + "=" * 50)
    print("********** LEADERBOARD **********")
    print("=" * 50 + "\n")
    if not rows:
        print("No quiz attempts yet.")
        return
    print(f"{'Rank':<6}{'User':<15}{'Category':<18}{'Score'}")
    print("-" * 50)
    for rank, row in enumerate(rows, start=1):
        score_str = f"{row['score']}/{row['total_questions']}"
        print(f"{rank:<6}{row['full_name']:<15}{row['category_name']:<18}{score_str}")

def logout():
    print("\nLogged out successfully.")
    print("Returning to main menu...")

def quiz_menu(connection, user):
    while True:
        print("\n" + "=" * 40)
        print("              QUIZ MENU")
        print("=" * 40)
        print("\n1. Start Quiz")
        print("2. Previous Results")
        print("3. Leaderboard")
        print("4. Logout")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            start_quiz(connection, user)
        elif choice == "2":
            show_previous_results(connection, user)
        elif choice == "3":
            show_leaderboard(connection)
        elif choice == "4":
            logout()
            break
        else:
            print("\nInvalid choice. Please try again.")

def main():
    """Program entry point: connect to MySQL, then loop the main menu."""
    connection = connect_database()
    if connection is None:
        print("Could not connect to the database. Please check DB_CONFIG and try again.")
        return
    try:
        while True:
            print("\n" + "=" * 40)
            print("          ONLINE QUIZ SYSTEM")
            print("=" * 40)
            print("\n1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("\nEnter your choice: ").strip()
            if choice == "1":
                register_user(connection)
            elif choice == "2":
                user = login_user(connection)
                if user:
                    quiz_menu(connection, user)
            elif choice == "3":
                print("\nThank you for using the Online Quiz System. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")
    finally:
        connection.close()



main()

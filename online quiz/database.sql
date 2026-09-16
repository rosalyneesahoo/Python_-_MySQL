
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

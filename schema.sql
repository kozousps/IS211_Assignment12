BEGIN TRANSACTION;
CREATE TABLE quizzes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            qs INTEGER NOT NULL,
            date TEXT NOT NULL);
DELETE FROM "sqlite_sequence";
CREATE TABLE student_result(
            studentid INTEGER NOT NULL,
            quizid INTEGER PRIMARY KEY AUTOINCREMENT,
            grade INTEGER NOT NULL,
            FOREIGN KEY (studentid) REFERENCES students (id),
            FOREIGN KEY (quizid) REFERENCES quizzes (id));
CREATE TABLE students(
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            id INTEGER PRIMARY KEY AUTOINCREMENT
            );
COMMIT;
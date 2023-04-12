CREATE TABLE IF NOT EXISTS Users (
    user_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    date_created TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    user_type TEXT NOT NULL DEFAULT "user"
);

CREATE TABLE IF NOT EXISTS Assessments (
    assessment_id TEXT PRIMARY KEY,
    competency_id TEXT NOT NULL,
    name TEXT UNIQUE NOT NULL,
    date_created TEXT NOT NULL,
    FOREIGN KEY (competency_id) REFERENCES Competencies (competency_id)
);

CREATE TABLE IF NOT EXISTS Competencies (
    competency_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    date_created TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS AssessmentResults (
    result_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    assessment_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    date_taken TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (assessment_id) REFERENCES Assessments (assessment_id),
    FOREIGN KEY (manager_id) REFERENCES Users (user_id)
)
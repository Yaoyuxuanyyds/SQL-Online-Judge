-- 用户表 (User)
CREATE TABLE User (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role INT NOT NULL CHECK (role IN (0, 1, 2)),
    UNIQUE (username)
);

-- 题目表 (Question)
CREATE TABLE Question (
    id INT PRIMARY KEY,
    title VARCHAR(1000) NOT NULL,
    create_sql TEXT NOT NULL,
    description TEXT NOT NULL,
    output_description TEXT NOT NULL,
    difficulty INT NOT NULL,
    standard_answer TEXT NOT NULL,
    is_public BOOLEAN NOT NULL DEFAULT TRUE
);

-- 考试表 (Exam)
CREATE TABLE Exam (
    id INT PRIMARY KEY,
    teacher_id INT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES User(id),
    CHECK (end_time > start_time)
);

-- 考试-题目表 (Exam_Question)
CREATE TABLE Exam_Question (
    exam_id INT,
    question_id INT,
    score INT NOT NULL DEFAULT 10 CHECK (score > 0),
    PRIMARY KEY (exam_id, question_id),
    FOREIGN KEY (exam_id) REFERENCES Exam(id),
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

-- 考试-学生表 (Exam_Student)
CREATE TABLE Exam_Student (
    exam_id INT,
    student_id INT,
    score INT NOT NULL DEFAULT 0 CHECK (score >= 0),
    PRIMARY KEY (exam_id, student_id),
    FOREIGN KEY (exam_id) REFERENCES Exam(id),
    FOREIGN KEY (student_id) REFERENCES User(id)
);

-- 测试用例表 (Test_Case)
CREATE TABLE Test_Case (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question_id INT,
    input_sql VARCHAR(255) NOT NULL,
    output VARCHAR(255) NOT NULL,
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

-- 提交表 (Submission)
CREATE TABLE Submission (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    exam_id INT,
    question_id INT,
    submit_sql TEXT NOT NULL,
    submit_time DATETIME NOT NULL,
    pass_rate FLOAT NOT NULL CHECK (pass_rate BETWEEN 0 AND 1),
    status INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES User(id),
    FOREIGN KEY (exam_id) REFERENCES Exam(id),
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

-- 文章表 (Article)
CREATE TABLE Article (
    id INT PRIMARY KEY,
    title VARCHAR(1000) NOT NULL,
    user_id INT,
    question_id INT,
    is_notice BOOLEAN NOT NULL,
    content TEXT NOT NULL,
    publish_time DATETIME NOT NULL,
    last_modify_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

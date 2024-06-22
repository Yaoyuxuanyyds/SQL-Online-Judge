create database sql_online_judge;
use sql_online_judge;

-- 用户表 (User)
create table User (
    id int primary key,
    username varchar(50) not null,
    password varchar(255) not null,
    role int not null check (role in (0, 1, 2)),
    session varchar(255),
    unique (username)
);

-- 题目表 (Question)
create table Question (
    id int auto_increment primary key,
    title varchar(1000) not null,
    create_code text not null,
    description text not null,
    output text not null,
    difficulty int not null,
    answer_example text not null,
    is_public boolean not null default true
);

-- 考试表 (Exam)
create table Exam (
    id int auto_increment primary key,
    teacher_id int,
    start_time datetime not null,
    end_time datetime not null,
    foreign key (teacher_id) references User(id),
    check (end_time > start_time)
);

-- 考试-题目表 (Exam_Question)
create table Exam_Question (
    exam_id int,
    question_id int,
    score int not null default 10 check (score > 0),
    primary key (exam_id, question_id),
    foreign key (exam_id) references Exam(id),
    foreign key (question_id) references Question(id)
);

-- 考试-学生表 (Exam_Student)
create table Exam_Student (
    exam_id int,
    student_id int,
    score int not null default 0 check (score >= 0),
    primary key (exam_id, student_id),
    foreign key (exam_id) references Exam(id),
    foreign key (student_id) references User(id)
);

-- 测试用例表 (Test_Case)
create table Test_Case (
    id int primary key auto_increment,
    question_id int,
    input_sql varchar(255) not null,
    output varchar(255) not null,
    foreign key (question_id) references Question(id)
);

-- 提交表 (Submission)
create table Submission (
    id int primary key auto_increment,
    student_id int,
    exam_id int,
    question_id int,
    submit_sql text not null,
    submit_time datetime not null,
    pass_rate float not null check (pass_rate between 0 and 1),
    status int not null,
    foreign key (student_id) references User(id),
    foreign key (exam_id) references Exam(id),
    foreign key (question_id) references Question(id)
);

-- 文章表 (Article)
create table Article (
    id int primary key,
    title varchar(1000) not null,
    user_id int,
    question_id int,
    is_notice boolean not null,
    content text not null,
    publish_time datetime not null,
    last_modify_time datetime not null default current_timestamp,
    foreign key (user_id) references User(id),
    foreign key (question_id) references Question(id)
);
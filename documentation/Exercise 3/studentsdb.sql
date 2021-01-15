CREATE DATABASE IF NOT EXISTS schooldb;

DROP TABLE IF EXISTS schooldb.students;

CREATE EXTERNAL TABLE schooldb.students
(
    school STRING,
    grade INT,
    student_number INT,
    `name` STRING,
    score INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
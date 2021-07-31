DROP TABLE IF EXISTS Tasks;

CREATE TABLE Tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_date text,
    task_time real,
    Title text,
    Description text,
    Done INTEGER,
    original_task_time text
);
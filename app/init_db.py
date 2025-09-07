from .db import get_connection, DB_FILE
schema_sql = """
CREATE TABLE IF NOT EXISTS colleges (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
college_id INTEGER,
name TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
FOREIGN KEY(college_id) REFERENCES colleges(id)
);

CREATE TABLE IF NOT EXISTS events (
id INTEGER PRIMARY KEY AUTOINCREMENT,
college_id INTEGER,
title TEXT NOT NULL,
type TEXT,
start_at TEXT,
end_at TEXT,
capacity INTEGER,
FOREIGN KEY(college_id) REFERENCES colleges(id)
);


CREATE TABLE IF NOT EXISTS registrations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id INTEGER,
event_id INTEGER,
UNIQUE(student_id, event_id),
FOREIGN KEY(student_id) REFERENCES students(id),
FOREIGN KEY(event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS attendance (
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id INTEGER,
event_id INTEGER,
checkin_time TEXT DEFAULT CURRENT_TIMESTAMP,
UNIQUE(student_id, event_id),
FOREIGN KEY(student_id) REFERENCES students(id),
FOREIGN KEY(event_id) REFERENCES events(id)
);


CREATE TABLE IF NOT EXISTS feedback (
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id INTEGER,
event_id INTEGER,
rating INTEGER CHECK(rating >=1 AND rating <=5),
comment TEXT,
UNIQUE(student_id, event_id),
FOREIGN KEY(student_id) REFERENCES students(id),
FOREIGN KEY(event_id) REFERENCES events(id)
);
"""

sample_data_sql = """
INSERT INTO colleges (name) VALUES ('College A');
INSERT INTO students (college_id, name, email) VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO events (college_id, title, type, start_at, end_at, capacity)
VALUES (1, 'AI Workshop', 'Workshop', '2025-09-10 10:00', '2025-09-10 12:00', 100);
"""

def main():
    if DB_FILE.exists():
        DB_FILE.unlink() # Reset DB each time for prototype
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(schema_sql)
    cur.executescript(sample_data_sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
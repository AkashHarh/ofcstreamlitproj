# import sqlite3

# DB_NAME = "course_management.db"


# def get_connection():
#     conn = sqlite3.connect(DB_NAME, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn


# def init_db():
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS courses (
#             course_id INTEGER PRIMARY KEY ,
#             course_name TEXT NOT NULL,
#             description TEXT,
#             duration TEXT,
#             is_active TEXT NOT NULL DEFAULT 'Yes',
#             created_at TEXT NOT NULL
#         );
#     """)

#     conn.commit()
#     conn.close()
#     print("Database ready")


# def close_connection(conn):
#     if conn:
#         conn.close()


# if __name__ == "__main__":
#     init_db()
#     print(f"{DB_NAME} created")





import sqlite3

DB_NAME = "course_management.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Courses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY  ,
            course_name TEXT NOT NULL,
            description TEXT,
            duration TEXT,
            is_active TEXT NOT NULL DEFAULT 'Yes',
            created_at TEXT NOT NULL
        );
    """)

    # Enrollments table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY ,
            course_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            enrolled_at TEXT NOT NULL,
            FOREIGN KEY(course_id) REFERENCES courses(course_id)
        );
    """)

    conn.commit()
    conn.close()
    print("Database ready")

if __name__ == "__main__":
    init_db()
    print(f"{DB_NAME} initialized")

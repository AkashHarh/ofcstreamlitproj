# from fastapi import FastAPI, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List
# from datetime import datetime
# import sqlite3

# from db import get_connection, init_db
# from model import (
#     CourseCreate,
#     CourseRead,
#     CourseUpdate,
#     CourseBase,
#     CourseDeleteResponse
# )

# init_db()

# app = FastAPI(
#     title="Course Management System API",
#     description="RESTful API for managing courses",
#     version="1.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def row_to_course(row: sqlite3.Row) -> CourseRead:
#     return CourseRead(**dict(row))


# @app.get("/", tags=["Root"])
# def root():
#     return {
#         "message": "Course Management System API",
#         "version": "1.0.0",
#         "status": "active",
#         "endpoints": {
#             "courses": "/courses",
#             "documentation": "/docs",
#             "redoc": "/redoc"
#         }
#     }


# @app.get("/courses", response_model=List[CourseRead], tags=["Courses"])
# def list_courses():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM courses ORDER BY course_id ASC")
#     rows = cur.fetchall()
#     conn.close()
#     return [row_to_course(row) for row in rows]


# @app.get("/courses/{course_id}", response_model=CourseRead, tags=["Courses"])
# def get_course(course_id: int):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
#     row = cur.fetchone()
#     conn.close()

#     if not row:
#         raise HTTPException(404, f"Course with ID {course_id} not found")

#     return row_to_course(row)


# @app.post("/courses", response_model=CourseRead, status_code=201)
# def create_course(course: CourseCreate):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT MAX(course_id) FROM courses")
#     max_id = cur.fetchone()[0]
#     next_id = 1 if max_id is None else max_id + 1

#     created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     cur.execute(
#         "INSERT INTO courses (course_id, course_name, description, duration, is_active, created_at) "
#         "VALUES (?, ?, ?, ?, ?, ?)",
#         (next_id, course.course_name, course.description, course.duration, course.is_active, created_at)
#     )
#     conn.commit()

#     cur.execute("SELECT * FROM courses WHERE course_id = ?", (next_id,))
#     row = cur.fetchone()
#     conn.close()

#     return row_to_course(row)



# @app.put("/courses/{course_id}", response_model=CourseRead, tags=["Courses"])
# def update_course(course_id: int, course: CourseBase):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
#     if not cur.fetchone():
#         conn.close()
#         raise HTTPException(404, f"Course with ID {course_id} not found")

#     cur.execute(
#         """
#         UPDATE courses
#         SET course_name = ?, description = ?, duration = ?, is_active = ?
#         WHERE course_id = ?
#         """,
#         (course.course_name, course.description, course.duration, course.is_active, course_id),
#     )
#     conn.commit()

#     cur.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
#     row = cur.fetchone()
#     conn.close()

#     return row_to_course(row)


# @app.patch("/courses/{course_id}", response_model=CourseRead, tags=["Courses"])
# def partial_update_course(course_id: int, course: CourseUpdate):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
#     row = cur.fetchone()
#     if not row:
#         conn.close()
#         raise HTTPException(404, f"Course with ID {course_id} not found")

#     existing = row_to_course(row).dict()
#     updates = course.dict(exclude_unset=True)
#     existing.update(updates)

#     cur.execute(
#         """
#         UPDATE courses
#         SET course_name = ?, description = ?, duration = ?, is_active = ?
#         WHERE course_id = ?
#         """,
#         (
#             existing["course_name"],
#             existing["description"],
#             existing["duration"],
#             existing["is_active"],
#             course_id,
#         ),
#     )
#     conn.commit()

#     cur.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
#     row = cur.fetchone()
#     conn.close()

#     return row_to_course(row)


# @app.delete("/courses/{course_id}", response_model=CourseDeleteResponse, tags=["Courses"])
# def delete_course(course_id: int):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT course_id FROM courses WHERE course_id = ?", (course_id,))
#     existing = cur.fetchone()

#     if existing is None:
#         conn.close()
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Course with ID {course_id} not found"
#         )

#     cur.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
#     conn.commit()
#     conn.close()

#     return CourseDeleteResponse(
#         success=True,
#         message=f"Course {course_id} deleted successfully",
#         course_id=course_id
#     )



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)




from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from datetime import datetime
import sqlite3

# Assuming db.py and model.py are available and contain necessary definitions
from db import get_connection, init_db
from model import (
    CourseCreate, CourseRead, CourseUpdate, CourseDeleteResponse,
    EnrollmentCreate, EnrollmentRead
)

init_db()
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

def convert_to_course(row: sqlite3.Row) -> CourseRead:
    return CourseRead(
        course_id=row["course_id"],
        course_name=row["course_name"],
        description=row["description"],
        duration=row["duration"],
        is_active=row["is_active"],
        created_at=row["created_at"]
    )

def convert_to_enrollment(row: sqlite3.Row) -> EnrollmentRead:
    return EnrollmentRead(
        enrollment_id=row["enrollment_id"],
        course_id=row["course_id"],
        student_name=row["student_name"],
        enrolled_at=row["enrolled_at"]
    )

# --- NEW DASHBOARD ENDPOINT ---
@app.get("/dashboard/summary", response_model=Dict[str, Any])
def get_dashboard_summary():
    """Retrieves summary statistics for the dashboard."""
    conn = get_connection()
    cur = conn.cursor()
    
    summary = {}
    
    try:
        # 1. Total Courses
        cur.execute("SELECT COUNT(course_id) FROM courses")
        summary["total_courses"] = cur.fetchone()[0]

        # 2. Active Courses
        cur.execute("SELECT COUNT(course_id) FROM courses WHERE is_active='Yes'")
        summary["active_courses"] = cur.fetchone()[0]

        # 3. Total Enrollments
        cur.execute("SELECT COUNT(enrollment_id) FROM enrollments")
        summary["total_enrollments"] = cur.fetchone()[0]
        
    finally:
        conn.close()
        
    return summary



@app.get("/courses", response_model=List[CourseRead])
def get_all_courses(
    is_active: Optional[str] = Query(None, description="Filter by 'Yes' or 'No'"),
    search: Optional[str] = Query(None, description="Search by course name or description")
):
    #Retrieves all courses, with filtering and searching
    conn = get_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM courses WHERE 1=1"
    params = []
    
    if is_active in ["Yes", "No"]:
        query += " AND is_active=?"
        params.append(is_active)
        
    if search:
        query += " AND (course_name LIKE ? OR description LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])
        
    query += " ORDER BY course_id ASC"

    try:
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
    finally:
        conn.close()
        
    return [convert_to_course(row) for row in rows]

@app.post("/courses", response_model=CourseRead)
def add_new_course(course: CourseCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT course_id FROM courses WHERE course_id=?", (course.course_id,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail=f"Course ID {course.course_id} already exists.")
        
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute(
            "INSERT INTO courses (course_id, course_name, description, duration, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (course.course_id, course.course_name, course.description, course.duration, course.is_active, created_at)
        )
        conn.commit()
        cur.execute("SELECT * FROM courses WHERE course_id=?", (course.course_id,))
        row = cur.fetchone()
    finally:
        conn.close()
        
    return convert_to_course(row)

@app.put("/courses/{course_id}", response_model=CourseRead)
def update_existing_course(course_id: int, course: CourseCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Course ID {course_id} not found.")

    try:
        cur.execute(
            "UPDATE courses SET course_name=?, description=?, duration=?, is_active=? WHERE course_id=?",
            (course.course_name, course.description, course.duration, course.is_active, course_id)
        )
        conn.commit()
        cur.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
        row = cur.fetchone()
    finally:
        conn.close()
        
    return convert_to_course(row)

@app.patch("/courses/{course_id}", response_model=CourseRead)
def partial_update_course(course_id: int, course: CourseUpdate):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
    existing_row = cur.fetchone()
    if not existing_row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Course ID {course_id} not found.")
    
    existing = convert_to_course(existing_row)
    updated_data = existing.model_dump()
    
    update_payload = course.model_dump(exclude_unset=True)
    updated_data.update(update_payload)
    
    try:
        cur.execute(
            "UPDATE courses SET course_name=?, description=?, duration=?, is_active=? WHERE course_id=?",
            (updated_data["course_name"], updated_data["description"], 
             updated_data["duration"], updated_data["is_active"], course_id)
        )
        conn.commit()
        cur.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
        row = cur.fetchone()
    finally:
        conn.close()
        
    return convert_to_course(row)

@app.delete("/courses/{course_id}", response_model=CourseDeleteResponse)
def remove_course(course_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Course ID {course_id} not found.")
        
    try:
        cur.execute("DELETE FROM courses WHERE course_id=?", (course_id,))
        conn.commit()
    finally:
        conn.close()
        
    return {"success": True, "message": "Course deleted successfully", "course_id": course_id}



@app.post("/enrollments", response_model=EnrollmentRead)
def add_new_enrollment(enroll: EnrollmentCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT enrollment_id FROM enrollments WHERE enrollment_id=?", (enroll.enrollment_id,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail=f"Enrollment ID {enroll.enrollment_id} already exists.")
    
    cur.execute("SELECT course_id FROM courses WHERE course_id=?", (enroll.course_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Course ID {enroll.course_id} not found. Cannot enroll.")

    enrolled_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute(
            "INSERT INTO enrollments (enrollment_id, course_id, student_name, enrolled_at) VALUES (?, ?, ?, ?)",
            (enroll.enrollment_id, enroll.course_id, enroll.student_name, enrolled_at)
        )
        conn.commit()
        cur.execute("SELECT * FROM enrollments WHERE enrollment_id=?", (enroll.enrollment_id,))
        row = cur.fetchone()
    finally:
        conn.close()
        
    return convert_to_enrollment(row)

@app.get("/enrollments", response_model=List[EnrollmentRead])
def get_all_enrollments():
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM enrollments ORDER BY enrollment_id ASC")
        rows = cur.fetchall()
    finally:
        conn.close()
        
    return [convert_to_enrollment(row) for row in rows]

@app.delete("/enrollments/{enroll_id}")
def remove_enrollment(enroll_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM enrollments WHERE enrollment_id=?", (enroll_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Enrollment ID {enroll_id} not found.")
        
    try:
        cur.execute("DELETE FROM enrollments WHERE enrollment_id=?", (enroll_id,))
        conn.commit()
    finally:
        conn.close()
        
    return {"success": True, "message": "Enrollment deleted successfully", "enrollment_id": enroll_id}



@app.get("/students/{student_name}/enrollments", response_model=List[EnrollmentRead])
def get_student_enrollments(student_name: str):
    #Retrieves all enrollments for a specific student
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "SELECT * FROM enrollments WHERE student_name=? ORDER BY enrolled_at DESC", 
            (student_name,)
        )
        rows = cur.fetchall()
    finally:
        conn.close()
        
    if not rows:
        raise HTTPException(status_code=404, detail=f"Student '{student_name}' has no active enrollments.")
        
    return [convert_to_enrollment(row) for row in rows]
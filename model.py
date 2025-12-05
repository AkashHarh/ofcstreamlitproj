# from pydantic import BaseModel, Field
# from typing import Optional, List


# class CourseBase(BaseModel):
#     course_name: str = None
#     description: Optional[str] = None
#     duration: Optional[str] = None
#     is_active: str = "Yes"


# class CourseCreate(CourseBase):
#     pass


# class CourseUpdate(BaseModel):
#     course_name: Optional[str] = None
#     description: Optional[str] = None
#     duration: Optional[str] = None
#     is_active: Optional[str] = None


# class CourseFullUpdate(CourseBase):
#     pass


# class CourseRead(CourseBase):
#     course_id: int
#     created_at: str


#     class Config:
#         orm_mode = True


# class CourseList(BaseModel):
#     total: int
#     courses: List[CourseRead]


# class CourseDeleteResponse(BaseModel):
#     success: bool
#     message: str
#     course_id: int


# class ErrorResponse(BaseModel):
#     success: bool = False
#     error: str
#     message: str
#     details: Optional[dict] = None


# class SuccessResponse(BaseModel):
#     success: bool = True
#     message: str
#     data: Optional[dict] = None


from pydantic import BaseModel, Field
from typing import Optional, List

class CourseBase(BaseModel):
    course_name: str = None
    description: Optional[str] = None
    duration: Optional[str] = None
    is_active: str = "Yes"

class CourseCreate(CourseBase):
    course_id: int

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    is_active: Optional[str] = None

class CourseRead(CourseBase):
    course_id: int
    created_at: str
    class Config:
        orm_mode = True

class CourseDeleteResponse(BaseModel):
    success: bool
    message: str
    course_id: int

class EnrollmentBase(BaseModel):
    course_id: int
    student_name: str

class EnrollmentCreate(EnrollmentBase):
    enrollment_id: int

class EnrollmentRead(EnrollmentBase):
    enrollment_id: int
    enrolled_at: str
    class Config:
        orm_mode = True

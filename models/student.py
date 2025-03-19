"""Student-related schemas for the Yale Degree Audit application."""

from datetime import date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, EmailStr


class Student(BaseModel):
    """Schema for student data."""
    student_id: int
    net_id: str
    first_name: str
    last_name: str
    class_year: int
    email: EmailStr
    
    @validator('class_year')
    def validate_class_year(cls, v):
        if v <= 0:
            raise ValueError('class_year must be greater than 0')
        return v
    
    @property
    def full_name(self) -> str:
        """Return the student's full name."""
        return f"{self.first_name} {self.last_name}"


class StudentEnrollment(BaseModel):
    """Schema for student course enrollment data."""
    enrollment_id: int
    student_id: int
    course_id: int
    term_taken: str
    grade: Optional[str] = None
    status: str
    
    # Relationship fields (for nested data)
    course: Optional[Dict[str, Any]] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class StudentMajor(BaseModel):
    """Schema for student major declaration data."""
    student_major_id: int
    student_id: int
    major_version_id: int
    declaration_date: date
    is_primary_major: bool = False
    
    # Relationship fields (for nested data)
    major_version: Optional[Dict[str, Any]] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class StudentCoursePlan(BaseModel):
    """Schema for student course plan data."""
    plan_id: int
    student_id: int
    course_id: int
    intended_term: str
    priority: Optional[int] = None
    notes: Optional[str] = None
    
    # Relationship fields (for nested data)
    course: Optional[Dict[str, Any]] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class StudentResponse(BaseModel):
    """Schema for student response data."""
    student: Student
    majors: List[StudentMajor] = []
    enrollments: List[StudentEnrollment] = []
    plans: Optional[List[StudentCoursePlan]] = None

"""Course-related schemas for the Yale Degree Audit application."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Course(BaseModel):
    """Schema for course data."""
    course_id: int
    subject_code: str
    course_number: str
    course_title: str
    description: Optional[str] = None
    credits: float
    distribution: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True
    
    @property
    def full_code(self) -> str:
        """Return the full course code."""
        return f"{self.subject_code} {self.course_number}"
    
    @property
    def full_title(self) -> str:
        """Return the full course title with code."""
        return f"{self.full_code}: {self.course_title}"


class CoursePrerequisite(BaseModel):
    """Schema for course prerequisite data."""
    course_id: int
    prereq_course_id: int
    concurrency_allowed: bool = False
    
    # Relationship fields (for nested data)
    prerequisite: Optional[Course] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class CoursePaginatedResponse(BaseModel):
    """Schema for paginated course response."""
    page: int
    per_page: int
    total: Optional[int] = None
    courses: List[Course]
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class EquivalenceGroup(BaseModel):
    """Schema for course equivalence group data."""
    eq_group_id: int
    group_name: str
    group_notes: Optional[str] = None
    
    # Relationship fields (for nested data)
    courses: Optional[List[Course]] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class EquivalenceGroupCourse(BaseModel):
    """Schema for mapping between equivalence groups and courses."""
    eq_group_course_id: int
    eq_group_id: int
    course_id: int
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True

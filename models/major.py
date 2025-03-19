"""Major-related schemas for the Yale Degree Audit application."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Major(BaseModel):
    """Schema for major data."""
    major_id: int
    major_name: str
    major_code: str
    department: str
    description: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class MajorVersion(BaseModel):
    """Schema for major version data."""
    major_version_id: int
    major_id: int
    catalog_year: int
    effective_term: str
    valid_until_term: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = None
    
    # Relationship fields (for nested data)
    major: Optional[Major] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class MajorRequirement(BaseModel):
    """Schema for major requirement data."""
    requirement_id: int
    major_version_id: int
    requirement_name: str
    requirement_type: str
    description: Optional[str] = None
    min_credits: float = 0
    max_credits: Optional[float] = None
    min_courses: int = 0
    max_courses: Optional[int] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class RequirementGroup(BaseModel):
    """Schema for requirement group data."""
    requirement_group_id: int
    requirement_id: int
    group_name: str
    group_operator: str = "AND"
    min_courses_in_group: int = 0
    max_courses_in_group: Optional[int] = None
    group_description: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class RequirementGroupCourse(BaseModel):
    """Schema for mapping between requirement groups and courses."""
    req_group_course_id: int
    requirement_group_id: int
    course_id: int
    is_required_in_group: bool = False
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class RequirementRule(BaseModel):
    """Schema for requirement rules data."""
    requirement_rule_id: int
    requirement_id: Optional[int] = None
    requirement_group_id: Optional[int] = None
    rule_type: str
    operator: str
    value: str
    notes: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class RequirementWithGroups(MajorRequirement):
    """Extended schema for requirement data with its groups."""
    groups: List[RequirementGroup] = []


class MajorRequirementsResponse(BaseModel):
    """Schema for major requirements response."""
    major_version: MajorVersion
    requirements: List[RequirementWithGroups]
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class MajorCoursesResponse(BaseModel):
    """Schema for major courses response."""
    major_version: MajorVersion
    courses: List[Dict[str, Any]]
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True

"""Degree audit schemas for the Yale Degree Audit application."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class UnfulfilledGroup(BaseModel):
    """Schema for unfulfilled group data in degree audit."""
    group_name: str
    courses_completed: int
    courses_required: int
    courses_remaining: int
    completed_courses: List[str]
    available_courses: List[str]
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class RuleViolation(BaseModel):
    """Schema for rule violation data in degree audit."""
    rule_type: str
    description: str
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class UnfulfilledRequirement(BaseModel):
    """Schema for unfulfilled requirement data in degree audit."""
    requirement_name: str
    unfulfilled_groups: List[UnfulfilledGroup]
    rule_violations: Optional[List[RuleViolation]] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class MajorUnfulfilledRequirement(BaseModel):
    """Schema for major's unfulfilled requirement data."""
    major: str
    requirement_name: str
    groups: List[UnfulfilledGroup]
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class DegreeAuditResponse(BaseModel):
    """Schema for degree audit response."""
    status: str
    unfulfilled_requirements: Optional[List[MajorUnfulfilledRequirement]] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True


class MajorCompletionResult(BaseModel):
    """Schema for the result of checking major completion."""
    is_completed: bool
    unfulfilled_requirements: List[UnfulfilledRequirement]
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True

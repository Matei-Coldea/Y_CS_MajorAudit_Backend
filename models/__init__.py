"""Pydantic model schemas for the Yale Degree Audit application."""

# Course models
from .course import (
    Course,
    CoursePrerequisite,
    CoursePaginatedResponse,
    EquivalenceGroup,
    EquivalenceGroupCourse
)

# Student models
from .student import (
    Student,
    StudentEnrollment,
    StudentMajor,
    StudentCoursePlan,
    StudentResponse
)

# Major models
from .major import (
    Major,
    MajorVersion,
    MajorRequirement,
    RequirementGroup,
    RequirementGroupCourse,
    RequirementRule,
    RequirementWithGroups,
    MajorRequirementsResponse,
    MajorCoursesResponse
)

# Degree audit models
from .degree_audit import (
    UnfulfilledGroup,
    RuleViolation,
    UnfulfilledRequirement,
    MajorUnfulfilledRequirement,
    DegreeAuditResponse,
    MajorCompletionResult
)

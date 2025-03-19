"""Service for course-related functionality."""

from typing import Dict, Any, List, Optional

from repositories.course_repository import CourseRepository
from models.course import CoursePaginatedResponse


class CourseService:
    """Service for course-related functionality."""
    
    def __init__(self, course_repository: CourseRepository):
        """
        Initialize with repositories.
        
        Args:
            course_repository: Repository for course data
        """
        self.course_repo = course_repository
    
    def get_all_courses(self, subject_code: Optional[str] = None, 
                         distribution: Optional[str] = None,
                         page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """
        Get all courses with optional filtering and pagination.
        
        Args:
            subject_code: Optional subject code to filter by
            distribution: Optional distribution requirement to filter by
            page: The page number
            per_page: The number of records per page
            
        Returns:
            Dictionary with pagination information and list of courses
        """
        return self.course_repo.get_paginated(
            page=page,
            per_page=per_page,
            subject_code=subject_code,
            distribution=distribution
        )
    
    def get_course_details(self, course_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a course, including prerequisites and equivalents.
        
        Args:
            course_id: The course ID
            
        Returns:
            Dictionary with course information, prerequisites, and equivalent courses
            
        Raises:
            ValueError: If the course is not found
        """
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise ValueError(f"Course not found with ID: {course_id}")
        
        # Get prerequisites
        prerequisites = self.course_repo.get_prerequisites(course_id)
        
        # Get equivalent courses
        equivalents = self.course_repo.get_equivalent_courses(course_id)
        
        return {
            'course': course,
            'prerequisites': prerequisites,
            'equivalents': equivalents
        }
    
    def search_courses(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for courses by title, subject code, or course number.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries representing the matching courses
        """
        # In a real implementation, you would use a more efficient search mechanism,
        # but for simplicity, we'll just filter in-memory
        
        # Get all courses (in a real app, you'd use a database search feature)
        all_courses = self.course_repo.get_all()
        
        # Filter courses by query
        query = query.lower()
        matching_courses = []
        
        for course in all_courses:
            title = course.get('course_title', '').lower()
            subject = course.get('subject_code', '').lower()
            number = course.get('course_number', '').lower()
            
            if (query in title or query in subject or query in number or
                query in f"{subject} {number}".lower()):
                matching_courses.append(course)
                
            if len(matching_courses) >= limit:
                break
        
        return matching_courses
    
    def get_courses_by_subject(self, subject_code: str) -> List[Dict[str, Any]]:
        """
        Get all courses for a specific subject.
        
        Args:
            subject_code: The subject code
            
        Returns:
            List of dictionaries representing the courses
        """
        return self.course_repo.filter_by(subject_code=subject_code)
    
    def get_courses_by_distribution(self, distribution: str) -> List[Dict[str, Any]]:
        """
        Get all courses that fulfill a specific distribution requirement.
        
        Args:
            distribution: The distribution requirement code
            
        Returns:
            List of dictionaries representing the courses
        """
        return self.course_repo.filter_by(distribution=distribution)

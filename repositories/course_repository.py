"""Repository for course-related database operations."""

from typing import List, Dict, Any, Optional
from supabase import Client

from .base import BaseRepository
from models.course import Course


class CourseRepository(BaseRepository[Course]):
    """Repository for course-related database operations."""
    
    def __init__(self, supabase_client: Client):
        """Initialize with Supabase client."""
        super().__init__(supabase_client, 'courses')
    
    def get_paginated(self, page: int = 1, per_page: int = 50, 
                      subject_code: Optional[str] = None, 
                      distribution: Optional[str] = None) -> Dict[str, Any]:
        """
        Get courses with pagination and optional filtering.
        
        Args:
            page: The page number (1-indexed)
            per_page: The number of records per page
            subject_code: Optional subject code to filter by
            distribution: Optional distribution requirement to filter by
            
        Returns:
            Dictionary with pagination information and list of courses
        """
        query = self.supabase.table(self.table_name).select('*')
        
        if subject_code:
            query = query.eq('subject_code', subject_code)
        
        if distribution:
            query = query.eq('distribution', distribution)
        
        # Calculate range for pagination
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        response = query.range(start, end).execute()
        
        # Get total count (simplified version - in a real app, you'd want to do this more efficiently)
        count_query = self.supabase.table(self.table_name).select('course_id')
        
        if subject_code:
            count_query = count_query.eq('subject_code', subject_code)
        
        if distribution:
            count_query = count_query.eq('distribution', distribution)
            
        count_response = count_query.execute()
        total = len(count_response.data) if count_response.data else 0
        
        return {
            'page': page,
            'per_page': per_page,
            'total': total,
            'courses': response.data if response.data else []
        }
    
    def get_by_ids(self, course_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get courses by list of IDs.
        
        Args:
            course_ids: List of course IDs
            
        Returns:
            List of dictionaries representing the courses
        """
        if not course_ids:
            return []
            
        response = self.supabase.table(self.table_name)\
            .select('course_id, subject_code, course_number, course_title')\
            .in_('course_id', course_ids)\
            .execute()
            
        return response.data if response.data else []
    
    def get_prerequisites(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Get all prerequisites for a course.
        
        Args:
            course_id: The course ID
            
        Returns:
            List of dictionaries representing the prerequisite courses
        """
        response = self.supabase.table('courseprerequisites')\
            .select('*, courses(*)')\
            .eq('course_id', course_id)\
            .execute()
            
        return response.data if response.data else []
    
    def get_group_courses(self, requirement_group_id: int) -> List[Dict[str, Any]]:
        """
        Get all courses for a requirement group.
        
        Args:
            requirement_group_id: The requirement group ID
            
        Returns:
            List of dictionaries representing the group courses
        """
        response = self.supabase.table('requirementgroupcourses')\
            .select('*')\
            .eq('requirement_group_id', requirement_group_id)\
            .execute()
            
        return response.data if response.data else []
    
    def get_equivalent_courses(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Get all equivalent courses for a given course.
        
        Args:
            course_id: The course ID
            
        Returns:
            List of dictionaries representing the equivalent courses
        """
        # First, find all equivalence groups this course belongs to
        groups_query = self.supabase.table('equivalencegroupcourses')\
            .select('eq_group_id')\
            .eq('course_id', course_id)\
            .execute()
            
        if not groups_query.data:
            return []
            
        eq_group_ids = [g['eq_group_id'] for g in groups_query.data]
        
        # Then, find all courses in those equivalence groups (except the original course)
        courses_query = self.supabase.table('equivalencegroupcourses')\
            .select('equivalencegroupcourses.course_id, courses.*')\
            .in_('eq_group_id', eq_group_ids)\
            .neq('course_id', course_id)\
            .join('courses', 'equivalencegroupcourses.course_id', 'courses.course_id')\
            .execute()
            
        return courses_query.data if courses_query.data else []

"""Repository for student-related database operations."""

from typing import List, Dict, Any, Optional
from supabase import Client

from .base import BaseRepository
from models.student import Student


class StudentRepository(BaseRepository[Student]):
    """Repository for student-related database operations."""
    
    def __init__(self, supabase_client: Client):
        """Initialize with Supabase client."""
        super().__init__(supabase_client, 'students')
    
    def get_by_net_id(self, net_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a student by NetID.
        
        Args:
            net_id: The student's NetID
            
        Returns:
            Dictionary representing the student, or None if not found
        """
        response = self.supabase.table(self.table_name).select('*').eq('net_id', net_id).execute()
        
        if response.data:
            return response.data[0]
        return None
    
    def get_declared_majors(self, student_id: int) -> List[Dict[str, Any]]:
        """
        Get all majors declared by a student.
        
        Args:
            student_id: The student's ID
            
        Returns:
            List of dictionaries representing the student's declared majors
        """
        response = self.supabase.table('studentmajors')\
            .select('*, majorversions(*, majors(*))')\
            .eq('student_id', student_id)\
            .execute()
            
        return response.data if response.data else []
    
    def get_course_enrollments(self, student_id: int, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all course enrollments for a student.
        
        Args:
            student_id: The student's ID
            status: Optional enrollment status to filter by (e.g., 'Completed', 'Enrolled')
            
        Returns:
            List of dictionaries representing the student's course enrollments
        """
        query = self.supabase.table('studentcourseenrollments')\
            .select('*')\
            .eq('student_id', student_id)
            
        if status:
            query = query.eq('status', status)
            
        response = query.execute()
        return response.data if response.data else []
    
    def get_completed_courses(self, student_id: int, course_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get completed courses for a student that match the given course IDs.
        
        Args:
            student_id: The student's ID
            course_ids: List of course IDs to check
            
        Returns:
            List of dictionaries representing the student's completed courses
        """
        if not course_ids:
            return []
            
        response = self.supabase.table('studentcourseenrollments')\
            .select('*')\
            .eq('student_id', student_id)\
            .eq('status', 'Completed')\
            .in_('course_id', course_ids)\
            .execute()
            
        return response.data if response.data else []
    
    def get_course_plans(self, student_id: int) -> List[Dict[str, Any]]:
        """
        Get all course plans for a student.
        
        Args:
            student_id: The student's ID
            
        Returns:
            List of dictionaries representing the student's course plans
        """
        response = self.supabase.table('studentcourseplans')\
            .select('*')\
            .eq('student_id', student_id)\
            .execute()
            
        return response.data if response.data else []

"""Service for student-related functionality."""

from typing import Dict, Any, List, Optional

from repositories.student_repository import StudentRepository
from repositories.course_repository import CourseRepository
from models.student import StudentResponse


class StudentService:
    """Service for student-related functionality."""
    
    def __init__(self, student_repository: StudentRepository, course_repository: CourseRepository):
        """
        Initialize with repositories.
        
        Args:
            student_repository: Repository for student data
            course_repository: Repository for course data
        """
        self.student_repo = student_repository
        self.course_repo = course_repository
    
    def get_student_info(self, net_id: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a student.
        
        Args:
            net_id: The student's NetID
            
        Returns:
            Dictionary with student information, declared majors, and course enrollments
            
        Raises:
            ValueError: If the student is not found
        """
        # Get student by NetID
        student = self.student_repo.get_by_net_id(net_id)
        if not student:
            raise ValueError(f"No student found with NetID: {net_id}")
        
        student_id = student['student_id']
        
        # Get student's declared majors
        majors = self.student_repo.get_declared_majors(student_id)
        
        # Get student's course enrollments
        enrollments = self.student_repo.get_course_enrollments(student_id)
        
        # Enhance enrollments with course details
        enrollments_with_details = []
        for enrollment in enrollments:
            course_id = enrollment['course_id']
            course = self.course_repo.get_by_id(course_id)
            
            if course:
                enrollment_with_details = enrollment.copy()
                enrollment_with_details['course'] = course
                enrollments_with_details.append(enrollment_with_details)
        
        # Get student's course plans
        plans = self.student_repo.get_course_plans(student_id)
        
        # Enhance plans with course details
        plans_with_details = []
        for plan in plans:
            course_id = plan['course_id']
            course = self.course_repo.get_by_id(course_id)
            
            if course:
                plan_with_details = plan.copy()
                plan_with_details['course'] = course
                plans_with_details.append(plan_with_details)
        
        # Construct the response
        result = {
            'student': student,
            'majors': majors,
            'enrollments': enrollments_with_details,
            'plans': plans_with_details
        }
        
        return result
    
    def get_student_enrollments(self, student_id: int, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all course enrollments for a student with course details.
        
        Args:
            student_id: The student's ID
            status: Optional enrollment status to filter by
            
        Returns:
            List of dictionaries representing the student's course enrollments with course details
        """
        enrollments = self.student_repo.get_course_enrollments(student_id, status)
        
        # Enhance enrollments with course details
        enrollments_with_details = []
        for enrollment in enrollments:
            course_id = enrollment['course_id']
            course = self.course_repo.get_by_id(course_id)
            
            if course:
                enrollment_with_details = enrollment.copy()
                enrollment_with_details['course'] = course
                enrollments_with_details.append(enrollment_with_details)
        
        return enrollments_with_details
    
    def calculate_student_gpa(self, student_id: int) -> float:
        """
        Calculate the GPA for a student based on completed courses.
        
        Args:
            student_id: The student's ID
            
        Returns:
            The calculated GPA
        """
        # Get completed enrollments with grades
        enrollments = self.student_repo.get_course_enrollments(student_id, 'Completed')
        
        # Create a dictionary mapping grades to credit hours
        grades_credits = {}
        
        for enrollment in enrollments:
            grade = enrollment.get('grade')
            if not grade:
                continue
                
            course_id = enrollment['course_id']
            course = self.course_repo.get_by_id(course_id)
            
            if not course:
                continue
                
            credits = course.get('credits', 0)
            
            if grade in grades_credits:
                grades_credits[grade] += credits
            else:
                grades_credits[grade] = credits
        
        # Calculate GPA (simplified version)
        total_points = 0
        total_credits = 0
        
        grade_values = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0
        }
        
        for grade, credits in grades_credits.items():
            if grade in grade_values:
                total_points += grade_values[grade] * credits
                total_credits += credits
        
        if total_credits == 0:
            return 0.0
            
        return round(total_points / total_credits, 2)

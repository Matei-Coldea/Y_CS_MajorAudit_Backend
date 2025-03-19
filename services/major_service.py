"""Service for major-related functionality."""

from typing import Dict, Any, List, Optional

from repositories.major_repository import MajorRepository
from repositories.course_repository import CourseRepository
from models.major import MajorRequirementsResponse, MajorCoursesResponse


class MajorService:
    """Service for major-related functionality."""
    
    def __init__(self, major_repository: MajorRepository, course_repository: CourseRepository):
        """
        Initialize with repositories.
        
        Args:
            major_repository: Repository for major data
            course_repository: Repository for course data
        """
        self.major_repo = major_repository
        self.course_repo = course_repository
    
    def get_all_majors(self) -> List[Dict[str, Any]]:
        """
        Get all available majors.
        
        Returns:
            List of dictionaries representing all majors
        """
        return self.major_repo.get_all()
    
    def get_major_by_id(self, major_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific major.
        
        Args:
            major_id: The major ID
            
        Returns:
            Dictionary with major information and latest version
            
        Raises:
            ValueError: If the major is not found
        """
        major = self.major_repo.get_by_id(major_id)
        if not major:
            raise ValueError(f"Major not found with ID: {major_id}")
        
        # Get the latest version of this major
        version = self.major_repo.get_active_version(major_id)
        
        result = major.copy()
        if version:
            result['latest_version'] = version
        
        return result
    
    def get_major_requirements(self, major_id: int, catalog_year: Optional[int] = None) -> Dict[str, Any]:
        """
        Get all requirements for a specific major.
        
        Args:
            major_id: The major ID
            catalog_year: Optional catalog year to filter by
            
        Returns:
            Dictionary with major version information and requirements
            
        Raises:
            ValueError: If the major version is not found
        """
        # Get the major version
        major_version = self.major_repo.get_active_version(major_id, catalog_year)
        if not major_version:
            raise ValueError(f"Major version not found for major ID: {major_id}")
        
        major_version_id = major_version['major_version_id']
        
        # Get requirements for this major version
        requirements = self.major_repo.get_requirements(major_version_id)
        
        # For each requirement, get its requirement groups
        requirements_with_groups = []
        for req in requirements:
            requirement_id = req['requirement_id']
            groups = self.major_repo.get_requirement_groups(requirement_id)
            
            req_with_groups = req.copy()
            req_with_groups['groups'] = groups
            requirements_with_groups.append(req_with_groups)
        
        return {
            'major_version': major_version,
            'requirements': requirements_with_groups
        }
    
    def get_major_courses(self, major_id: int, requirement_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all courses that can fulfill requirements for a specific major.
        
        Args:
            major_id: The major ID
            requirement_type: Optional requirement type to filter by
            
        Returns:
            Dictionary with major version information and courses
            
        Raises:
            ValueError: If the major version is not found or no courses are found
        """
        # Get the active major version
        major_version = self.major_repo.get_active_version(major_id)
        if not major_version:
            raise ValueError(f"Major version not found for major ID: {major_id}")
        
        major_version_id = major_version['major_version_id']
        
        # Get requirements filtered by type if specified
        requirements = self.major_repo.get_requirements(major_version_id, requirement_type)
        
        if not requirements:
            raise ValueError(f"No requirements found for this major")
        
        # Get all requirement groups for these requirements
        requirement_ids = [req['requirement_id'] for req in requirements]
        
        all_groups = []
        for req_id in requirement_ids:
            groups = self.major_repo.get_requirement_groups(req_id)
            all_groups.extend(groups)
        
        if not all_groups:
            raise ValueError(f"No requirement groups found for this major")
        
        # Get all courses for these requirement groups
        group_ids = [group['requirement_group_id'] for group in all_groups]
        
        all_course_ids = set()
        for group_id in group_ids:
            group_courses = self.course_repo.get_group_courses(group_id)
            for course in group_courses:
                all_course_ids.add(course['course_id'])
        
        if not all_course_ids:
            raise ValueError(f"No courses found for this major")
        
        # Get course details
        course_details = []
        for course_id in all_course_ids:
            course = self.course_repo.get_by_id(course_id)
            if course:
                course_details.append(course)
        
        return {
            'major_version': major_version,
            'courses': course_details
        }

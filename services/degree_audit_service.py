"""Service for degree audit functionality."""

from typing import Dict, Any, List, Optional

from repositories.student_repository import StudentRepository
from repositories.major_repository import MajorRepository
from repositories.course_repository import CourseRepository
from repositories.distribution_repository import DistributionRepository
from services.distribution_service import DistributionService
from models.degree_audit import DegreeAuditResponse, MajorCompletionResult
from utils.grade_utils import meets_min_grade, extract_course_level


class DegreeAuditService:
    """Service for degree audit functionality."""
    
    def __init__(self, student_repository: StudentRepository, 
                 major_repository: MajorRepository,
                 course_repository: CourseRepository,
                 distribution_repository: DistributionRepository):
        """
        Initialize with repositories.
        
        Args:
            student_repository: Repository for student data
            major_repository: Repository for major data
            course_repository: Repository for course data
            distribution_repository: Repository for distribution data
        """
        self.student_repo = student_repository
        self.major_repo = major_repository
        self.course_repo = course_repository
        self.distribution_service = DistributionService(
            distribution_repository,
            student_repository,
            course_repository
        )
    
    def check_degree_completion(self, net_id: str) -> Dict[str, Any]:
        """
        Check if a student has completed their major requirements and distribution requirements.
        
        Args:
            net_id: The student's NetID
            
        Returns:
            Dictionary with completion status, unfulfilled major requirements,
            and distribution requirements status
            
        Raises:
            ValueError: If the student is not found or has no declared majors
        """
        # Get student info
        student = self.student_repo.get_by_net_id(net_id)
        if not student:
            raise ValueError(f"No student found with NetID: {net_id}")
        
        student_id = student['student_id']
        
        # Get student's declared majors
        student_majors = self.student_repo.get_declared_majors(student_id)
        if not student_majors:
            raise ValueError(f"Student has no declared majors")
        
        # Process each major
        all_completed = True
        unfulfilled_requirements = []
        
        for student_major in student_majors:
            major_name = student_major['majorversions']['majors']['major_name']
            result = self.check_major_completion_with_details(student_id, student_major)
            
            if not result['is_completed']:
                all_completed = False
                
                # Add unfulfilled requirements to the list
                for req in result['unfulfilled_requirements']:
                    unfulfilled_requirements.append({
                        'major': major_name,
                        'requirement_name': req['requirement_name'],
                        'groups': req['unfulfilled_groups']
                    })
        
        # Get distribution requirements status
        distribution_status = self.distribution_service.get_student_distribution_status(student_id)
        
        # Check if all distribution requirements are met
        distribution_completed = True
        for year_progress in distribution_status['year_progress'].values():
            if not year_progress['is_fulfilled']:
                distribution_completed = False
                break
        
        # Determine overall completion status
        all_completed = all_completed and distribution_completed
        completion_status = "Completed" if all_completed else "Not Completed"
        
        # Build response
        response = {
            'status': completion_status,
            'major_requirements': {
                'status': "Completed" if all_completed else "Not Completed"
            },
            'distribution_requirements': {
                'status': "Completed" if distribution_completed else "Not Completed",
                'current_year': distribution_status['current_year'],
                'current_year_requirements_fulfilled': distribution_status['current_year_requirements_fulfilled'],
                'year_progress': distribution_status['year_progress'],
                'distribution_totals': distribution_status['distribution_totals']
            }
        }
        
        # Only include unfulfilled major requirements if there are any
        if not all_completed:
            response['major_requirements']['unfulfilled_requirements'] = unfulfilled_requirements
        
        return response
    
    def check_major_completion_with_details(self, student_id: int, student_major: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a student has completed all requirements for a specific major,
        and return details about any unfulfilled requirements.
        
        Args:
            student_id: The student's ID
            student_major: The student's major data from the database
            
        Returns:
            Dictionary with completion status and unfulfilled requirements
        """
        major_version_id = student_major['major_version_id']
        
        # Get all requirements for this major version
        requirements = self.major_repo.get_requirements(major_version_id)
        
        if not requirements:
            return {
                'is_completed': False,
                'unfulfilled_requirements': [
                    {
                        'requirement_name': 'No requirements found',
                        'unfulfilled_groups': []
                    }
                ]
            }
        
        # Check each requirement
        all_requirements_met = True
        unfulfilled_requirements = []
        
        for requirement in requirements:
            requirement_id = requirement['requirement_id']
            requirement_name = requirement['requirement_name']
            
            # Get all requirement groups for this requirement
            groups = self.major_repo.get_requirement_groups(requirement_id)
            
            if not groups:
                continue
            
            # Check each requirement group
            requirement_met = True
            unfulfilled_groups = []
            
            for group in groups:
                group_id = group['requirement_group_id']
                group_name = group['group_name']
                min_courses = group['min_courses_in_group']
                
                # Get courses that belong to this requirement group
                group_courses = self.course_repo.get_group_courses(group_id)
                
                if not group_courses:
                    continue
                
                # Get the course IDs that can fulfill this requirement
                course_ids = [item['course_id'] for item in group_courses]
                
                # Get courses information
                courses_info = self.course_repo.get_by_ids(course_ids)
                courses_info_dict = {course['course_id']: course for course in courses_info}
                
                # Get completed courses that fulfill this requirement
                completed_courses = self.student_repo.get_completed_courses(student_id, course_ids)
                courses_completed = len(completed_courses)
                group_met = courses_completed >= min_courses
                
                if not group_met:
                    requirement_met = False
                    
                    # Get available courses for this group
                    available_courses = []
                    for course_id in course_ids:
                        if course_id in courses_info_dict:
                            course = courses_info_dict[course_id]
                            course_label = f"{course['subject_code']} {course['course_number']}: {course['course_title']}"
                            available_courses.append(course_label)
                    
                    # Get courses already completed
                    completed_course_labels = []
                    for enrollment in completed_courses:
                        course_id = enrollment['course_id']
                        if course_id in courses_info_dict:
                            course = courses_info_dict[course_id]
                            course_label = f"{course['subject_code']} {course['course_number']}: {course['course_title']}"
                            completed_course_labels.append(course_label)
                    
                    # Add unfulfilled group info
                    unfulfilled_groups.append({
                        'group_name': group_name,
                        'courses_completed': courses_completed,
                        'courses_required': min_courses,
                        'courses_remaining': min_courses - courses_completed,
                        'completed_courses': completed_course_labels,
                        'available_courses': available_courses
                    })
            
            if not requirement_met:
                all_requirements_met = False
                
                # Add unfulfilled requirement info
                unfulfilled_requirements.append({
                    'requirement_name': requirement_name,
                    'unfulfilled_groups': unfulfilled_groups
                })
        
        # Check additional rules if all standard requirements are met
        rule_violations = []
        
        if all_requirements_met:
            rules = self.major_repo.get_requirement_rules(major_version_id)
            
            for rule in rules:
                rule_violation = None
                
                # Process each rule type
                if rule['rule_type'] == 'MIN_GRADE':
                    passes_rule = self._check_min_grade_rule(student_id, rule)
                    if not passes_rule:
                        all_requirements_met = False
                        rule_violation = {
                            'rule_type': 'Minimum Grade Requirement',
                            'description': rule['notes'] or f"Minimum grade of {rule['value']} required"
                        }
                
                elif rule['rule_type'] == 'COURSE_LEVEL':
                    passes_rule = self._check_course_level_rule(student_id, rule)
                    if not passes_rule:
                        all_requirements_met = False
                        rule_violation = {
                            'rule_type': 'Course Level Requirement',
                            'description': rule['notes'] or f"Minimum of {rule['value']} level courses required"
                        }
                
                if rule_violation:
                    rule_violations.append(rule_violation)
        
        # Add rule violations to unfulfilled requirements if any
        if rule_violations:
            unfulfilled_requirements.append({
                'requirement_name': 'Additional Requirements',
                'unfulfilled_groups': [],
                'rule_violations': rule_violations
            })
        
        return {
            'is_completed': all_requirements_met,
            'unfulfilled_requirements': unfulfilled_requirements
        }
    
    def _check_min_grade_rule(self, student_id: int, rule: Dict[str, Any]) -> bool:
        """
        Check if a student meets the minimum grade requirement for certain courses.
        
        Args:
            student_id: The student's ID
            rule: The requirement rule dictionary
            
        Returns:
            Boolean indicating if the rule is satisfied
        """
        # Get courses associated with the rule
        courses_to_check = self.major_repo.get_rule_courses(rule)
        
        if not courses_to_check:
            return True  # No courses to check
        
        # Get student's completed courses that match
        completed_courses = self.student_repo.get_completed_courses(student_id, courses_to_check)
        
        if not completed_courses:
            return False  # No completed courses in this category
        
        # Check if all completed courses meet the minimum grade requirement
        min_grade = rule['value']  # e.g., 'B-'
        for enrollment in completed_courses:
            if not meets_min_grade(enrollment['grade'], min_grade):
                return False
        
        return True
    
    def _check_course_level_rule(self, student_id: int, rule: Dict[str, Any]) -> bool:
        """
        Check if a student has taken enough courses at or above a specified level.
        
        Args:
            student_id: The student's ID
            rule: The requirement rule dictionary
            
        Returns:
            Boolean indicating if the rule is satisfied
        """
        # Get courses associated with the rule
        courses_to_check = self.major_repo.get_rule_courses(rule)
        
        if not courses_to_check:
            return True  # No courses to check
        
        # Get student's completed courses
        completed_courses = self.student_repo.get_completed_courses(student_id, courses_to_check)
        
        if not completed_courses:
            return False  # No completed courses
        
        # Get course information for completed courses
        course_details = []
        for enrollment in completed_courses:
            course_id = enrollment['course_id']
            course = self.course_repo.get_by_id(course_id)
            if course:
                course_details.append(course)
        
        # Count how many courses are at or above the required level
        min_level = int(rule['value'])  # e.g., '400'
        high_level_courses = 0
        
        for course in course_details:
            course_number = course['course_number']
            level = extract_course_level(course_number)
            
            if level and level >= min_level:
                high_level_courses += 1
        
        # Check against the rule requirements
        operator = rule['operator']
        required_count = 1  # Default, but could be specified in the rule
        
        if operator == '>=':
            return high_level_courses >= required_count
        elif operator == '=':
            return high_level_courses == required_count
        elif operator == '>':
            return high_level_courses > required_count
        
        return False
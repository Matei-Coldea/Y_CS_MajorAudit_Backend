"""Service for distribution requirement functionality."""

from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime

from repositories.distribution_repository import DistributionRepository
from repositories.student_repository import StudentRepository
from repositories.course_repository import CourseRepository


class DistributionService:
    """Service for tracking Yale's tiered distributional requirements."""
    
    def __init__(self, distribution_repository: DistributionRepository,
                 student_repository: StudentRepository,
                 course_repository: CourseRepository):
        """
        Initialize with repositories.
        
        Args:
            distribution_repository: Repository for distribution requirement data
            student_repository: Repository for student data
            course_repository: Repository for course data
        """
        self.dist_repo = distribution_repository
        self.student_repo = student_repository
        self.course_repo = course_repository
        
        # Cache distribution types
        self.distribution_types = self._get_distribution_types()
        
        # Cache academic years
        self.academic_years = self._get_academic_years()
        
        # Cache requirements for each year
        self.requirements_by_year = self._get_distribution_requirements()
        
        # Cache special rules
        self.year_rules = self._get_year_rules()
    
    def _get_distribution_types(self) -> Dict[str, Dict[str, Any]]:
        """Get distribution types from database."""
        types = self.dist_repo.get_distribution_types()
        return {item['code']: item for item in types}
    
    def _get_academic_years(self) -> Dict[str, Dict[str, Any]]:
        """Get academic years from database."""
        years = self.dist_repo.get_academic_years()
        return {item['name']: item for item in years}
    
    def _get_distribution_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get distribution requirements for each year."""
        # Get all requirements
        requirements = self.dist_repo.get_distribution_requirements()
        
        # Organize by year
        requirements_by_year = {}
        for item in requirements:
            year_name = item['academicyears']['name']
            dist_code = item['distributiontypes']['code']
            
            if year_name not in requirements_by_year:
                requirements_by_year[year_name] = {
                    'description': self.academic_years[year_name]['description'],
                    'requirements': {}
                }
            
            requirements_by_year[year_name]['requirements'][dist_code] = item['courses_required']
        
        return requirements_by_year
    
    def _get_year_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get special rules for each year."""
        # Get all rules
        rules = self.dist_repo.get_year_rules()
        
        # Organize by year
        rules_by_year = {}
        for rule in rules:
            year_name = rule['academicyears']['name']
            
            if year_name not in rules_by_year:
                rules_by_year[year_name] = []
            
            rules_by_year[year_name].append(rule)
        
        return rules_by_year
    
    def determine_year_label(self, student: Dict[str, Any]) -> str:
        """
        Determine a student's current year (Freshman, Sophomore, etc.).
        
        Args:
            student: The student data dictionary
            
        Returns:
            String representing the academic year (Freshman, Sophomore, etc.)
        """
        current_year = datetime.now().year
        class_year = student['class_year']
        years_to_go = class_year - current_year
        
        if years_to_go >= 3:
            return "Freshman"
        elif years_to_go == 2:
            return "Sophomore"
        elif years_to_go == 1:
            return "Junior"
        else:
            return "Senior"
    
    def _optimize_distribution_assignments(
        self,
        courses_with_distributions: List[Tuple[int, List[str]]],
        requirements: Dict[str, int]
    ) -> Dict[int, str]:
        """
        Optimize how courses are assigned to fulfill distribution requirements.
        
        Args:
            courses_with_distributions: List of tuples (course_id, list of possible distribution codes)
            requirements: Dictionary of {distribution_code: number_required}
            
        Returns:
            Dictionary mapping course_id to assigned distribution code
        """
        # Copy requirements to track remaining needs
        remaining_requirements = requirements.copy()
        
        # Track which distribution has been assigned to each course
        assignments = {}
        
        # First pass: Handle courses with only one distribution type
        for course_id, dist_codes in courses_with_distributions:
            if len(dist_codes) == 1 and dist_codes[0] in remaining_requirements:
                code = dist_codes[0]
                if remaining_requirements[code] > 0:
                    assignments[course_id] = code
                    remaining_requirements[code] -= 1
        
        # Second pass: Handle courses with multiple distribution types
        # Sort courses by number of distribution options (fewer options first)
        multi_dist_courses = [
            (course_id, dist_codes) 
            for course_id, dist_codes in courses_with_distributions 
            if len(dist_codes) > 1 and course_id not in assignments
        ]
        multi_dist_courses.sort(key=lambda x: len(x[1]))
        
        for course_id, dist_codes in multi_dist_courses:
            # Find the distribution type with highest remaining need
            best_code = None
            highest_need = -1
            
            for code in dist_codes:
                if code in remaining_requirements and remaining_requirements[code] > highest_need:
                    best_code = code
                    highest_need = remaining_requirements[code]
            
            # If we found a needed distribution type, assign it
            if best_code and highest_need > 0:
                assignments[course_id] = best_code
                remaining_requirements[best_code] -= 1
            # If no specific need, assign to first available type
            elif not best_code and dist_codes:
                assignments[course_id] = dist_codes[0]
        
        return assignments

    def get_student_distribution_status(self, student_id: int) -> Dict[str, Any]:
        """
        Get a student's distribution requirement status by year.
        
        Args:
            student_id: The student ID
            
        Returns:
            Dictionary with detailed distribution status information
        """
        # Get student info to determine year
        student = self.student_repo.get_by_id(student_id)
        current_year_label = self.determine_year_label(student)
        
        # Get completed courses
        enrollments = self.student_repo.get_course_enrollments(student_id, "Completed")
        
        # Collect courses and their possible distribution types
        courses_with_distributions = []
        for enrollment in enrollments:
            course_id = enrollment['course_id']
            course = self.course_repo.get_by_id(course_id)
            
            if course and course.get('distribution'):
                dist_codes = [code.strip() for code in course['distribution'].split(',')]
                courses_with_distributions.append((course_id, dist_codes))
        
        # Initialize fulfilled counts for all distribution types
        fulfilled_counts = {code: 0 for code in self.distribution_types.keys()}
        
        # Track which distribution requirement each course fulfills
        course_assignments = {}
        
        # Process requirements year by year
        year_progress = {}
        for year, year_config in self.requirements_by_year.items():
            requirements = year_config["requirements"]
            
            # Get special rules for this year
            year_rules = self.year_rules.get(year, [])
            
            # Optimize distribution assignments for this year's requirements
            year_assignments = self._optimize_distribution_assignments(
                courses_with_distributions,
                {code: req for code, req in requirements.items()}
            )
            
            # Update fulfilled counts based on assignments
            for course_id, assigned_code in year_assignments.items():
                if assigned_code in fulfilled_counts:
                    fulfilled_counts[assigned_code] += 1
                    course_assignments[course_id] = assigned_code
            
            # Calculate fulfillment status
            min_categories = len(requirements)
            for rule in year_rules:
                if rule['rule_type'] == 'MIN_CATEGORIES':
                    min_categories = rule['value']
            
            categories_fulfilled = sum(1 for code, required in requirements.items() 
                                    if fulfilled_counts[code] >= required)
            
            is_fulfilled = categories_fulfilled >= min_categories
            
            # Create year progress entry
            year_progress[year] = {
                "description": year_config["description"],
                "is_fulfilled": is_fulfilled,
                "categories_fulfilled": categories_fulfilled,
                "categories_required": min_categories,
                "category_details": {
                    code: {
                        "name": self.distribution_types[code]['name'],
                        "fulfilled": fulfilled_counts[code],
                        "required": req,
                        "is_complete": fulfilled_counts[code] >= req,
                        "courses": [
                            course_id for course_id, assigned_code 
                            in course_assignments.items() 
                            if assigned_code == code
                        ]
                    } for code, req in requirements.items()
                }
            }
        
        # Determine overall progress
        current_year_fulfilled = year_progress[current_year_label]["is_fulfilled"]
        
        results = {
            "current_year": current_year_label,
            "current_year_requirements_fulfilled": current_year_fulfilled,
            "year_progress": year_progress,
            "distribution_totals": {
                code: {
                    "name": self.distribution_types[code]['name'],
                    "completed_courses": fulfilled_counts[code],
                    "graduation_requirement": self.requirements_by_year["Senior"]["requirements"][code],
                    "courses": [
                        course_id for course_id, assigned_code 
                        in course_assignments.items() 
                        if assigned_code == code
                    ]
                } for code in self.distribution_types.keys()
            }
        }
        
        return results
    
    def get_distribution_status_by_year(self, student_id: int, year: str) -> Dict[str, Any]:
        """
        Get a student's distribution requirement status for a specific year.
        
        Args:
            student_id: The student ID
            year: The academic year (Freshman, Sophomore, etc.)
            
        Returns:
            Dictionary with distribution status for the specified year
        """
        # Get overall status first (more efficient than duplicating code)
        status = self.get_student_distribution_status(student_id)
        
        # Extract just the requested year's details
        if year not in status['year_progress']:
            raise ValueError(f"Invalid academic year: {year}")
        
        year_status = {
            'year': year,
            'description': status['year_progress'][year]['description'],
            'is_fulfilled': status['year_progress'][year]['is_fulfilled'],
            'categories_fulfilled': status['year_progress'][year]['categories_fulfilled'],
            'categories_required': status['year_progress'][year]['categories_required'],
            'category_details': status['year_progress'][year]['category_details']
        }
        
        return year_status
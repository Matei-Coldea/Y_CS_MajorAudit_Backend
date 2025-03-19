"""Utility functions for handling and calculating grades."""

from typing import Dict, Optional


# Grade value mapping (from highest to lowest)
GRADE_VALUES: Dict[str, int] = {
    'A+': 12, 'A': 11, 'A-': 10,
    'B+': 9, 'B': 8, 'B-': 7,
    'C+': 6, 'C': 5, 'C-': 4,
    'D+': 3, 'D': 2, 'D-': 1,
    'F': 0
}


def meets_min_grade(actual_grade: Optional[str], min_grade: str) -> bool:
    """
    Check if an actual grade meets or exceeds the minimum required grade.
    
    Args:
        actual_grade: The actual grade received (can be None)
        min_grade: The minimum grade required
        
    Returns:
        bool: True if the actual grade meets or exceeds the minimum grade, False otherwise
    """
    if actual_grade is None:
        return False
        
    if actual_grade not in GRADE_VALUES or min_grade not in GRADE_VALUES:
        return False
    
    return GRADE_VALUES[actual_grade] >= GRADE_VALUES[min_grade]


def calculate_gpa(grades: Dict[str, float]) -> float:
    """
    Calculate GPA based on letter grades and credits.
    
    Args:
        grades: Dictionary mapping letter grades to credit hours
        
    Returns:
        float: Calculated GPA
    """
    total_points = 0.0
    total_credits = 0.0
    
    for grade, credits in grades.items():
        if grade in GRADE_VALUES:
            # Convert to 4.0 scale (assuming A = 4.0, B = 3.0, etc.)
            gpa_value = min(4.0, GRADE_VALUES[grade] / 3.0)
            total_points += gpa_value * credits
            total_credits += credits
    
    if total_credits == 0:
        return 0.0
        
    return round(total_points / total_credits, 2)


def extract_course_level(course_number: str) -> Optional[int]:
    """
    Extract the numeric level from a course number (e.g., '401' from 'CPSC 401').
    
    Args:
        course_number: The course number string (e.g., '401', 'CS401', 'MATH 101A')
        
    Returns:
        int: The numeric level of the course, or None if no level can be extracted
    """
    # Extract digits only
    digits = ''.join(char for char in course_number if char.isdigit())
    
    if not digits:
        return None
    
    # Return the first 1-3 digits (course level)
    return int(digits[:3])

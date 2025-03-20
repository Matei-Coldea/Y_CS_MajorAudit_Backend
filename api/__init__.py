"""API routes for the Yale Degree Audit application."""

from .degree_audit import degree_audit_bp
from .majors import majors_bp
from .courses import courses_bp
from .students import students_bp
from .student_courses import student_courses_bp  
from .distributions import distributions_bp  

# List all blueprints
blueprints = [
    degree_audit_bp,
    majors_bp,
    courses_bp,
    students_bp,
    student_courses_bp,
    distributions_bp  
]
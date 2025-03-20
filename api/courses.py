"""API routes for course-related functionality."""

from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError

from services.course_service import CourseService


# Create Blueprint
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


@courses_bp.route('', methods=['GET'])
def get_all_courses():
    """
    Get a list of all courses with optional filtering.
    
    Returns:
        JSON response with paginated courses
    """
    try:
        # Get the course service from the app context
        course_service = current_app.course_service
        
        # Get query parameters for filtering and pagination
        subject_code = request.args.get('subject_code')
        distribution = request.args.get('distribution')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Get courses
        courses = course_service.get_all_courses(subject_code, distribution, page, per_page)
        
        if not courses['courses']:
            return jsonify({'message': 'No courses found'}), 404
        
        return jsonify(courses)
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving courses: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    """
    Get detailed information about a specific course.
    
    Args:
        course_id: The course ID
        
    Returns:
        JSON response with course details
    """
    try:
        # Get the course service from the app context
        course_service = current_app.course_service
        
        # Get course details
        course = course_service.get_course_details(course_id)
        return jsonify(course)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving course: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@courses_bp.route('/search', methods=['GET'])
def search_courses():
    """
    Search for courses by title, subject code, or course number.
    
    Returns:
        JSON response with matching courses
    """
    try:
        # Get the course service from the app context
        course_service = current_app.course_service
        
        # Get query parameter
        query = request.args.get('q', '')
        limit = request.args.get('limit', 10, type=int)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search courses
        courses = course_service.search_courses(query, limit)
        
        if not courses:
            return jsonify({'message': 'No matching courses found'}), 404
        
        return jsonify(courses)
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error searching courses: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@courses_bp.route('/subject/<subject_code>', methods=['GET'])
def get_courses_by_subject(subject_code):
    """
    Get all courses for a specific subject.
    
    Args:
        subject_code: The subject code
        
    Returns:
        JSON response with courses for the subject
    """
    try:
        # Get the course service from the app context
        course_service = current_app.course_service
        
        # Get courses by subject
        courses = course_service.get_courses_by_subject(subject_code)
        
        if not courses:
            return jsonify({'message': f'No courses found for subject: {subject_code}'}), 404
        
        return jsonify(courses)
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving courses by subject: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@courses_bp.route('/distribution/<distribution>', methods=['GET'])
def get_courses_by_distribution(distribution):
    """
    Get all courses that fulfill a specific distribution requirement.
    
    Args:
        distribution: The distribution requirement code
        
    Returns:
        JSON response with courses for the distribution requirement
    """
    try:
        # Get the course service from the app context
        course_service = current_app.course_service
        
        # Get courses by distribution
        courses = course_service.get_courses_by_distribution(distribution)
        
        if not courses:
            return jsonify({'message': f'No courses found for distribution: {distribution}'}), 404
        
        return jsonify(courses)
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving courses by distribution: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

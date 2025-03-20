"""API routes for student-related functionality."""

from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError

from services.student_service import StudentService


# Create Blueprint
students_bp = Blueprint('students', __name__, url_prefix='/api/students')


@students_bp.route('', methods=['GET'])
def get_student_info():
    """
    Get information about a specific student.
    
    Headers:
        X-Student-NetID: The student's NetID (required)
        
    Returns:
        JSON response with student information
    """
    try:
        # Get student NetID from header
        net_id = request.headers.get('X-Student-NetID')
        
        # Get the student service from the app context
        student_service = current_app.student_service
        
        # Get student info
        student_info = student_service.get_student_info(net_id)
        return jsonify(student_info)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving student info: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@students_bp.route('/enrollments', methods=['GET'])
def get_student_enrollments():
    """
    Get all course enrollments for a student.
    
    Headers:
        X-Student-NetID: The student's NetID (required)
        
    Query Parameters:
        status: Optional filter for enrollment status
        
    Returns:
        JSON response with student enrollments
    """
    try:
        # Get student NetID from header
        net_id = request.headers.get('X-Student-NetID')
        
        # Get the student service from the app context
        student_service = current_app.student_service
        
        # Get status filter if provided
        status = request.args.get('status')
        
        # First get the student to find their ID
        student_info = student_service.get_student_info(net_id)
        student_id = student_info['student']['student_id']
        
        # Get enrollments
        enrollments = student_service.get_student_enrollments(student_id, status)
        
        return jsonify(enrollments)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving student enrollments: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@students_bp.route('/gpa', methods=['GET'])
def get_student_gpa():
    """
    Calculate the GPA for a student.
    
    Headers:
        X-Student-NetID: The student's NetID (required)
        
    Returns:
        JSON response with student GPA
    """
    try:
        # Get student NetID from header
        net_id = request.headers.get('X-Student-NetID')
        
        # Get the student service from the app context
        student_service = current_app.student_service
        
        # First get the student to find their ID
        student_info = student_service.get_student_info(net_id)
        student_id = student_info['student']['student_id']
        
        # Calculate GPA
        gpa = student_service.calculate_student_gpa(student_id)
        
        return jsonify({'student_id': student_id, 'net_id': net_id, 'gpa': gpa})
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error calculating student GPA: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

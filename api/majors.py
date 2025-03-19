"""API routes for major-related functionality."""

from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError

from services.major_service import MajorService


# Create Blueprint
majors_bp = Blueprint('majors', __name__, url_prefix='/api/majors')


@majors_bp.route('', methods=['GET'])
def get_all_majors():
    """
    Get a list of all available majors.
    
    Returns:
        JSON response with list of majors
    """
    try:
        # Get the major service from the app context
        major_service = current_app.major_service
        
        # Get all majors
        majors = major_service.get_all_majors()
        
        if not majors:
            return jsonify({'message': 'No majors found'}), 404
        
        return jsonify(majors)
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving majors: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@majors_bp.route('/<int:major_id>', methods=['GET'])
def get_major_by_id(major_id):
    """
    Get detailed information about a specific major.
    
    Args:
        major_id: The major ID
        
    Returns:
        JSON response with major details
    """
    try:
        # Get the major service from the app context
        major_service = current_app.major_service
        
        # Get major by ID
        major = major_service.get_major_by_id(major_id)
        return jsonify(major)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving major: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@majors_bp.route('/<int:major_id>/requirements', methods=['GET'])
def get_major_requirements(major_id):
    """
    Get all requirements for a specific major.
    
    Args:
        major_id: The major ID
        
    Returns:
        JSON response with major requirements
    """
    try:
        # Get the major service from the app context
        major_service = current_app.major_service
        
        # Check if catalog year is provided as a query parameter
        catalog_year = request.args.get('catalog_year', type=int)
        
        # Get major requirements
        requirements = major_service.get_major_requirements(major_id, catalog_year)
        return jsonify(requirements)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving major requirements: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@majors_bp.route('/<int:major_id>/courses', methods=['GET'])
def get_major_courses(major_id):
    """
    Get all courses that can fulfill requirements for a specific major.
    
    Args:
        major_id: The major ID
        
    Returns:
        JSON response with major courses
    """
    try:
        # Get the major service from the app context
        major_service = current_app.major_service
        
        # Check if requirement type is provided as a query parameter
        requirement_type = request.args.get('type')
        
        # Get major courses
        courses = major_service.get_major_courses(major_id, requirement_type)
        return jsonify(courses)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving major courses: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

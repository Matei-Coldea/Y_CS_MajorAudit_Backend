"""API routes for distribution requirement functionality."""

from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError

from services.distribution_service import DistributionService
from utils.auth import auth_required  # If you have this


# Create Blueprint
distributions_bp = Blueprint('distributions', __name__, url_prefix='/api/distribution-requirements')


@distributions_bp.route('/<string:net_id>', methods=['GET'])
@auth_required
def get_distribution_requirements(net_id):
    """
    Get detailed distribution requirement status for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    Returns:
        JSON response with distribution requirement status by year
    """
    try:
        # Get student info
        student_info = current_app.student_service.get_student_info(net_id)
        student_id = student_info['student']['student_id']
        
        # Get distribution service
        dist_service = current_app.distribution_service
        
        # Get distribution status
        status = dist_service.get_student_distribution_status(student_id)
        
        return jsonify({
            'student_id': student_id,
            'net_id': net_id,
            'distribution_requirements': status
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting distribution requirements: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@distributions_bp.route('/<string:net_id>/<string:year>', methods=['GET'])
@auth_required
def get_distribution_requirements_by_year(net_id, year):
    """
    Get distribution requirement status for a student for a specific academic year.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    URL Parameters:
        year: The academic year to check (Freshman, Sophomore, Junior, Senior)
        
    Returns:
        JSON response with distribution requirement status for the specified year
    """
    # Validate year parameter
    valid_years = ["Freshman", "Sophomore", "Junior", "Senior"]
    if year not in valid_years:
        return jsonify({
            'error': 'Invalid year parameter',
            'message': f'Year must be one of: {", ".join(valid_years)}'
        }), 400
    
    try:
        # Get student info
        student_info = current_app.student_service.get_student_info(net_id)
        student_id = student_info['student']['student_id']
        
        # Get distribution service
        dist_service = current_app.distribution_service
        
        # Get distribution status for specified year
        year_status = dist_service.get_distribution_status_by_year(student_id, year)
        
        return jsonify({
            'student_id': student_id,
            'net_id': net_id,
            'distribution_requirements': year_status
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        current_app.logger.error(f"Error getting distribution requirements for {year}: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500
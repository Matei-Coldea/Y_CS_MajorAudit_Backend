"""API routes for degree audit functionality."""

from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError

from services.degree_audit_service import DegreeAuditService


# Create Blueprint
degree_audit_bp = Blueprint('degree_audit', __name__, url_prefix='/api')


@degree_audit_bp.route('/degree-audit', methods=['GET'])
def check_degree_completion():
    """
    Endpoint to check if a student has completed their major requirements.
    Requires the student's net_id in the request header.
    
    Returns:
        JSON response with completion status and unfulfilled requirements
    """
    # Get student net_id from request header
    net_id = request.headers.get('X-Student-NetID')
    
    if not net_id:
        return jsonify({
            'error': 'Missing student NetID in request header',
            'message': 'Please provide X-Student-NetID header'
        }), 400
    
    try:
        # Get the degree audit service from the app context
        degree_audit_service = current_app.degree_audit_service
        
        # Check degree completion
        result = degree_audit_service.check_degree_completion(net_id)
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'message': str(e)
        }), 404
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error checking degree completion: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': f'An error occurred while checking degree completion'
        }), 500

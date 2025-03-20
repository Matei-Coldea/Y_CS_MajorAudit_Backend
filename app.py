"""Yale Degree Audit Application - Main Entry Point."""

import os
import logging
from flask import Flask, request, jsonify
from supabase import create_client

from config import active_config
from api import blueprints
from repositories import StudentRepository, MajorRepository, CourseRepository , DistributionRepository
from services import StudentService, MajorService, CourseService, DegreeAuditService, DistributionService


from repositories.distribution_repository import DistributionRepository
def create_app(config=None):
    """
    Create and configure the Flask application.
    
    Args:
        config: Optional configuration object
        
    Returns:
        Configured Flask application
    """
    # Initialize Flask application
    app = Flask(__name__)
    
    # Configure the application
    if config is None:
        config = active_config
        
    app.config.from_object(config)
    
    # Validate configuration
    config.validate()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize Supabase client
    supabase = create_client(
        app.config['SUPABASE_URL'],
        app.config['SUPABASE_KEY']
    )
    
    # Store Supabase client in app config for direct access in routes
    app.config['supabase'] = supabase
    
    # Initialize repositories
    student_repo = StudentRepository(supabase)
    major_repo = MajorRepository(supabase)
    course_repo = CourseRepository(supabase)
    distribution_repo = DistributionRepository(supabase)
    
    # Initialize services
    app.student_service = StudentService(student_repo, course_repo)
    app.major_service = MajorService(major_repo, course_repo)
    app.course_service = CourseService(course_repo)
    app.degree_audit_service = DegreeAuditService(student_repo, major_repo, course_repo)
    app.distribution_service = DistributionService(  # Add this block
        distribution_repo,
        student_repo,
        course_repo
    )

    
    # Register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    # Add middleware for authentication
    @app.before_request
    def authenticate_request():
        # Skip authentication for excluded paths
        excluded_paths = ['/health']
        if request.path in excluded_paths:
            return None
        
        # Skip OPTIONS requests (for CORS preflight)
        if request.method == 'OPTIONS':
            return None
        
        # Get student NetID from header
        net_id = request.headers.get('X-Student-NetID')
        
        if not net_id:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required. Please provide X-Student-NetID header'
            }), 401
        
        # Get Supabase client
        supabase = app.config['supabase']
        
        try:
            # Check if student exists and is logged in
            response = supabase.table('students')\
                .select('*')\
                .eq('net_id', net_id)\
                .eq('logged', True)\
                .execute()
            
            if not response.data:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'User is not logged in or does not exist'
                }), 401
            
            # Store the student data in request for later use
            request.student = response.data[0]
        except Exception as e:
            app.logger.error(f"Authentication error: {str(e)}")
            return jsonify({
                'error': 'Authentication error',
                'message': 'An error occurred during authentication'
            }), 500
    
    # Add CORS support
    @app.after_request
    def add_cors_headers(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Student-NetID')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Add health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy', 'service': 'yale-degree-audit'}, 200
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return {'error': 'Not found', 'message': 'The requested resource was not found'}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors."""
        app.logger.error(f"Server error: {str(error)}")
        return {'error': 'Server error', 'message': 'An internal server error occurred'}, 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors."""
        return {'error': 'Method not allowed', 'message': 'The method is not allowed for the requested URL'}, 405
    
    return app


def main():
    """Run the application."""
    # Get port from environment variable or use default
    port = active_config.PORT
    
    # Create and run the application
    app = create_app()
    app.run(host='127.0.0.1', port=port, debug=app.config['DEBUG'])


if __name__ == '__main__':
    main()




# Hosting : https://replit.com/
# https://www.pythonanywhere.com/
# Refactor the database and include all majors
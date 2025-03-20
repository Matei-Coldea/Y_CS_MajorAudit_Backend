"""Yale Degree Audit Application - Main Entry Point."""

import os
import sys
import logging
from flask import Flask, request, jsonify
from supabase import create_client

from config import active_config
from api import blueprints
from repositories import StudentRepository, MajorRepository, CourseRepository, DistributionRepository
from services import StudentService, MajorService, CourseService, DegreeAuditService, DistributionService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def create_app(config=None):
    """
    Create and configure the Flask application.
    
    Args:
        config: Optional configuration object
        
    Returns:
        Configured Flask application
    """
    try:
        # Initialize Flask application
        app = Flask(__name__)
        
        # Configure the application
        if config is None:
            config = active_config
            
        app.config.from_object(config)
        
        # Validate configuration
        config.validate()
        
        logger.info("Starting application with configuration: %s", config.__name__)
        
        try:
            # Initialize Supabase client
            supabase = create_client(
                app.config['SUPABASE_URL'],
                app.config['SUPABASE_KEY']
            )
            logger.info("Successfully initialized Supabase client")
        except Exception as e:
            logger.error("Failed to initialize Supabase client: %s", str(e))
            raise
        
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
        app.degree_audit_service = DegreeAuditService(
            student_repo,
            major_repo,
            course_repo,
            distribution_repo
        )
        app.distribution_service = DistributionService(
            distribution_repo,
            student_repo,
            course_repo
        )
        
        logger.info("Successfully initialized all services")
        
        # Register blueprints
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
            logger.info("Registered blueprint: %s", blueprint.name)
        
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
                logger.error("Authentication error: %s", str(e))
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
            logger.error("Server error: %s", str(error))
            return {'error': 'Server error', 'message': 'An internal server error occurred'}, 500
        
        @app.errorhandler(405)
        def method_not_allowed(error):
            """Handle 405 errors."""
            return {'error': 'Method not allowed', 'message': 'The method is not allowed for the requested URL'}, 405
        
        logger.info("Application setup completed successfully")
        return app
        
    except Exception as e:
        logger.error("Failed to create application: %s", str(e))
        raise

def main():
    """Run the application."""
    try:
        port = int(os.environ.get("PORT", 5000))
        app = create_app()
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error("Failed to run application: %s", str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()




# Hosting : https://replit.com/
# https://www.pythonanywhere.com/
# Refactor the database and include all majors
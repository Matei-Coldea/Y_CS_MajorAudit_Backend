from functools import wraps
from flask import request, jsonify, current_app

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get student NetID from header
        net_id = request.headers.get('X-Student-NetID')
        
        if not net_id:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required. Please provide X-Student-NetID header'
            }), 401
        
        # Get Supabase client
        supabase = current_app.config['supabase']
        
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
        
        return f(*args, **kwargs)
    return decorated_function
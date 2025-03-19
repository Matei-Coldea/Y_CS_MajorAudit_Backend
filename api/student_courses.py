"""API routes for student course management (enrollments and plans)."""

from flask import Blueprint, request, jsonify, current_app
from pydantic import BaseModel, ValidationError, Field
from typing import Optional, List
from datetime import datetime


# Create Blueprint
student_courses_bp = Blueprint('student_courses', __name__, url_prefix='/api/student/courses')


# Models for request validation
class EnrollmentRequest(BaseModel):
    """Schema for course enrollment request."""
    course_id: int
    term_taken: str
    grade: Optional[str] = None
    status: str = "Enrolled"  # Default status


class CoursesPlanRequest(BaseModel):
    """Schema for course plan request."""
    course_id: int
    intended_term: str
    priority: Optional[int] = None
    notes: Optional[str] = None


class CoursesListRequest(BaseModel):
    """Schema for course list request."""
    course_ids: List[int]


# Helper function to validate student NetID from header
def get_student_id_from_header():
    """Get student ID from NetID in header."""
    net_id = request.headers.get('X-Student-NetID')
    
    if not net_id:
        return jsonify({
            'error': 'Missing student NetID in request header',
            'message': 'Please provide X-Student-NetID header'
        }), 400
    
    # Get the student service from the app context
    student_service = current_app.student_service
    
    try:
        # Get student info to find the ID
        student_info = student_service.get_student_info(net_id)
        student_id = student_info['student']['student_id']
        return student_id
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        current_app.logger.error(f"Error getting student ID: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/enrollments', methods=['GET'])
def get_enrollments():
    """
    Get all course enrollments for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    Query Parameters:
        status: Optional enrollment status to filter by (e.g., 'Completed', 'Enrolled')
        
    Returns:
        JSON response with student enrollments
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Get status filter if provided
        status = request.args.get('status')
        
        # Get the student service from the app context
        student_service = current_app.student_service
        
        # Get enrollments
        enrollments = student_service.get_student_enrollments(student_id, status)
        
        return jsonify(enrollments)
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving enrollments: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/enrollments', methods=['POST'])
def add_enrollment():
    """
    Add a new course enrollment for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    Request Body:
        course_id: The course ID
        term_taken: The term the course was taken (e.g., 'Fall 2022')
        grade: The grade received (optional)
        status: The enrollment status (default: 'Enrolled')
        
    Returns:
        JSON response with the created enrollment
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Parse and validate request data
        data = request.json
        enrollment_request = EnrollmentRequest(**data)
        
        # TODO: Implement add_student_enrollment in student_service
        # For now, we'll create a placeholder implementation
        
        # Check if the course exists
        course_service = current_app.course_service
        try:
            course = course_service.get_course_details(enrollment_request.course_id)
        except ValueError:
            return jsonify({'error': f'Course with ID {enrollment_request.course_id} not found'}), 404
        
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # Insert the enrollment
        enrollment_data = {
            'student_id': student_id,
            'course_id': enrollment_request.course_id,
            'term_taken': enrollment_request.term_taken,
            'grade': enrollment_request.grade,
            'status': enrollment_request.status
        }
        
        response = supabase.table('studentcourseenrollments').insert(enrollment_data).execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to create enrollment'}), 500
        
        new_enrollment = response.data[0]
        
        # Add course information to the response
        new_enrollment['course'] = course['course']
        
        return jsonify(new_enrollment), 201
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error creating enrollment: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/enrollments/<int:enrollment_id>', methods=['PUT'])
def update_enrollment(enrollment_id):
    """
    Update an existing course enrollment for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    URL Parameters:
        enrollment_id: The enrollment ID to update
        
    Request Body:
        term_taken: The term the course was taken (optional)
        grade: The grade received (optional)
        status: The enrollment status (optional)
        
    Returns:
        JSON response with the updated enrollment
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Parse and validate request data
        data = request.json
        
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # First check if the enrollment exists and belongs to this student
        check_response = supabase.table('studentcourseenrollments')\
            .select('*')\
            .eq('enrollment_id', enrollment_id)\
            .eq('student_id', student_id)\
            .execute()
        
        if not check_response.data:
            return jsonify({
                'error': 'Enrollment not found',
                'message': f'No enrollment found with ID {enrollment_id} for this student'
            }), 404
        
        # Prepare update data (only include fields that were provided)
        update_data = {}
        if 'term_taken' in data:
            update_data['term_taken'] = data['term_taken']
        if 'grade' in data:
            update_data['grade'] = data['grade']
        if 'status' in data:
            update_data['status'] = data['status']
        
        if not update_data:
            return jsonify({'error': 'No update data provided'}), 400
        
        # Update the enrollment
        response = supabase.table('studentcourseenrollments')\
            .update(update_data)\
            .eq('enrollment_id', enrollment_id)\
            .eq('student_id', student_id)\
            .execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to update enrollment'}), 500
        
        updated_enrollment = response.data[0]
        
        # Get course information
        course_service = current_app.course_service
        try:
            course = course_service.get_course_details(updated_enrollment['course_id'])
            updated_enrollment['course'] = course['course']
        except ValueError:
            # If we can't get course details, just return the enrollment without course info
            pass
        
        return jsonify(updated_enrollment)
        
    except Exception as e:
        current_app.logger.error(f"Error updating enrollment: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/enrollments/<int:enrollment_id>', methods=['DELETE'])
def delete_enrollment(enrollment_id):
    """
    Delete a course enrollment for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    URL Parameters:
        enrollment_id: The enrollment ID to delete
        
    Returns:
        JSON response confirming deletion
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # First check if the enrollment exists and belongs to this student
        check_response = supabase.table('studentcourseenrollments')\
            .select('*')\
            .eq('enrollment_id', enrollment_id)\
            .eq('student_id', student_id)\
            .execute()
        
        if not check_response.data:
            return jsonify({
                'error': 'Enrollment not found',
                'message': f'No enrollment found with ID {enrollment_id} for this student'
            }), 404
        
        # Delete the enrollment
        response = supabase.table('studentcourseenrollments')\
            .delete()\
            .eq('enrollment_id', enrollment_id)\
            .eq('student_id', student_id)\
            .execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to delete enrollment'}), 500
        
        return jsonify({
            'message': 'Enrollment deleted successfully',
            'enrollment_id': enrollment_id
        })
        
    except Exception as e:
        current_app.logger.error(f"Error deleting enrollment: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/plans', methods=['GET'])
def get_course_plans():
    """
    Get all course plans for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    Returns:
        JSON response with student course plans
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # Get all plans for this student
        response = supabase.table('studentcourseplans')\
            .select('*')\
            .eq('student_id', student_id)\
            .execute()
        
        if not response.data:
            return jsonify([])
        
        plans = response.data
        
        # Add course information to each plan
        course_service = current_app.course_service
        plans_with_details = []
        
        for plan in plans:
            course_id = plan['course_id']
            try:
                course = course_service.get_course_details(course_id)
                plan_with_details = plan.copy()
                plan_with_details['course'] = course['course']
                plans_with_details.append(plan_with_details)
            except ValueError:
                # If we can't get course details, still include the plan without course info
                plans_with_details.append(plan)
        
        return jsonify(plans_with_details)
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving course plans: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/plans', methods=['POST'])
def add_course_plan():
    """
    Add a new course plan for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    Request Body:
        course_id: The course ID
        intended_term: The term the student intends to take the course
        priority: Priority level (optional)
        notes: Additional notes (optional)
        
    Returns:
        JSON response with the created course plan
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Parse and validate request data
        data = request.json
        plan_request = CoursesPlanRequest(**data)
        
        # Check if the course exists
        course_service = current_app.course_service
        try:
            course = course_service.get_course_details(plan_request.course_id)
        except ValueError:
            return jsonify({'error': f'Course with ID {plan_request.course_id} not found'}), 404
        
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # Insert the course plan
        plan_data = {
            'student_id': student_id,
            'course_id': plan_request.course_id,
            'intended_term': plan_request.intended_term,
            'priority': plan_request.priority,
            'notes': plan_request.notes
        }
        
        response = supabase.table('studentcourseplans').insert(plan_data).execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to create course plan'}), 500
        
        new_plan = response.data[0]
        
        # Add course information to the response
        new_plan['course'] = course['course']
        
        return jsonify(new_plan), 201
        
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        current_app.logger.error(f"Error creating course plan: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/plans/<int:plan_id>', methods=['PUT'])
def update_course_plan(plan_id):
    """
    Update an existing course plan for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    URL Parameters:
        plan_id: The plan ID to update
        
    Request Body:
        intended_term: The term the student intends to take the course (optional)
        priority: Priority level (optional)
        notes: Additional notes (optional)
        
    Returns:
        JSON response with the updated course plan
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Parse request data
        data = request.json
        
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # First check if the plan exists and belongs to this student
        check_response = supabase.table('studentcourseplans')\
            .select('*')\
            .eq('plan_id', plan_id)\
            .eq('student_id', student_id)\
            .execute()
        
        if not check_response.data:
            return jsonify({
                'error': 'Course plan not found',
                'message': f'No course plan found with ID {plan_id} for this student'
            }), 404
        
        # Prepare update data (only include fields that were provided)
        update_data = {}
        if 'intended_term' in data:
            update_data['intended_term'] = data['intended_term']
        if 'priority' in data:
            update_data['priority'] = data['priority']
        if 'notes' in data:
            update_data['notes'] = data['notes']
        
        if not update_data:
            return jsonify({'error': 'No update data provided'}), 400
        
        # Update the course plan
        response = supabase.table('studentcourseplans')\
            .update(update_data)\
            .eq('plan_id', plan_id)\
            .eq('student_id', student_id)\
            .execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to update course plan'}), 500
        
        updated_plan = response.data[0]
        
        # Get course information
        course_service = current_app.course_service
        try:
            course = course_service.get_course_details(updated_plan['course_id'])
            updated_plan['course'] = course['course']
        except ValueError:
            # If we can't get course details, just return the plan without course info
            pass
        
        return jsonify(updated_plan)
        
    except Exception as e:
        current_app.logger.error(f"Error updating course plan: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/plans/<int:plan_id>', methods=['DELETE'])
def delete_course_plan(plan_id):
    """
    Delete a course plan for a student.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    URL Parameters:
        plan_id: The plan ID to delete
        
    Returns:
        JSON response confirming deletion
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # First check if the plan exists and belongs to this student
        check_response = supabase.table('studentcourseplans')\
            .select('*')\
            .eq('plan_id', plan_id)\
            .eq('student_id', student_id)\
            .execute()
        
        if not check_response.data:
            return jsonify({
                'error': 'Course plan not found',
                'message': f'No course plan found with ID {plan_id} for this student'
            }), 404
        
        # Delete the course plan
        response = supabase.table('studentcourseplans')\
            .delete()\
            .eq('plan_id', plan_id)\
            .eq('student_id', student_id)\
            .execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to delete course plan'}), 500
        
        return jsonify({
            'message': 'Course plan deleted successfully',
            'plan_id': plan_id
        })
        
    except Exception as e:
        current_app.logger.error(f"Error deleting course plan: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/batch/add-enrollments', methods=['POST'])
def batch_add_enrollments():
    """
    Add multiple course enrollments for a student in a single request.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    Request Body:
        enrollments: List of enrollment objects, each containing:
            course_id: The course ID
            term_taken: The term the course was taken
            grade: The grade received (optional)
            status: The enrollment status (optional, default: 'Enrolled')
            
    Returns:
        JSON response with the created enrollments
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Parse request data
        data = request.json
        if not data or 'enrollments' not in data or not isinstance(data['enrollments'], list):
            return jsonify({'error': 'Invalid request. Expected "enrollments" array.'}), 400
        
        # Validate each enrollment
        enrollments_to_add = []
        for enrollment_data in data['enrollments']:
            try:
                enrollment = EnrollmentRequest(**enrollment_data)
                enrollments_to_add.append({
                    'student_id': student_id,
                    'course_id': enrollment.course_id,
                    'term_taken': enrollment.term_taken,
                    'grade': enrollment.grade,
                    'status': enrollment.status
                })
            except ValidationError as e:
                return jsonify({
                    'error': f'Validation error in enrollment data: {enrollment_data}',
                    'message': str(e)
                }), 400
        
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # Insert the enrollments
        response = supabase.table('studentcourseenrollments').insert(enrollments_to_add).execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to create enrollments'}), 500
        
        # Add course information to the response
        course_service = current_app.course_service
        enrollments_with_details = []
        
        for enrollment in response.data:
            course_id = enrollment['course_id']
            try:
                course = course_service.get_course_details(course_id)
                enrollment_with_details = enrollment.copy()
                enrollment_with_details['course'] = course['course']
                enrollments_with_details.append(enrollment_with_details)
            except ValueError:
                # If we can't get course details, still include the enrollment without course info
                enrollments_with_details.append(enrollment)
        
        return jsonify({
            'message': f'Successfully added {len(enrollments_with_details)} enrollments',
            'enrollments': enrollments_with_details
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error adding enrollments in batch: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@student_courses_bp.route('/batch/delete-enrollments', methods=['POST'])
def batch_delete_enrollments():
    """
    Delete multiple course enrollments for a student in a single request.
    
    Headers:
        X-Student-NetID: The student's NetID
        
    Request Body:
        enrollment_ids: List of enrollment IDs to delete
            
    Returns:
        JSON response confirming deletion
    """
    student_id = get_student_id_from_header()
    if not isinstance(student_id, int):
        return student_id  # This is an error response
    
    try:
        # Parse request data
        data = request.json
        if not data or 'enrollment_ids' not in data or not isinstance(data['enrollment_ids'], list):
            return jsonify({'error': 'Invalid request. Expected "enrollment_ids" array.'}), 400
        
        enrollment_ids = data['enrollment_ids']
        
        # Connect to the database
        supabase = current_app.config['supabase']
        
        # First check which enrollments exist and belong to this student
        in_clause = f"({','.join([str(id) for id in enrollment_ids])})"
        check_response = supabase.table('studentcourseenrollments')\
            .select('enrollment_id')\
            .eq('student_id', student_id)\
            .in_('enrollment_id', enrollment_ids)\
            .execute()
        
        if not check_response.data:
            return jsonify({
                'error': 'Enrollments not found',
                'message': 'No enrollments found with the provided IDs for this student'
            }), 404
        
        # Get the IDs that were found
        found_ids = [enrollment['enrollment_id'] for enrollment in check_response.data]
        
        # Delete the enrollments
        response = supabase.table('studentcourseenrollments')\
            .delete()\
            .eq('student_id', student_id)\
            .in_('enrollment_id', found_ids)\
            .execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to delete enrollments'}), 500
        
        deleted_count = len(response.data)
        not_found = [id for id in enrollment_ids if id not in found_ids]
        
        return jsonify({
            'message': f'Successfully deleted {deleted_count} enrollments',
            'deleted_ids': found_ids,
            'not_found_ids': not_found
        })
        
    except Exception as e:
        current_app.logger.error(f"Error deleting enrollments in batch: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500
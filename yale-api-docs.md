# Yale Degree Audit API Documentation

## Overview

The Yale Degree Audit API is a RESTful service that provides programmatic access to student academic information, degree requirements, and audit functionality. This API allows students, advisors, and administrative systems to retrieve and manage academic data to evaluate progress toward graduation.

## Base URL

```
https://api.yaledegreeaudit.com/
```

## Authentication

All API endpoints (except `/health`) require authentication using the student's NetID. Authentication is implemented using a global middleware that verifies the student's login status in the database.

### Authentication Method

Include the student's NetID in the request header:

```
X-Student-NetID: abc123
```

The API verifies that:
1. The NetID exists in the database
2. The student's "logged" status is set to TRUE

### Authentication Responses

- **401 Unauthorized**: Returned when:
  - The X-Student-NetID header is missing
  - The student with the provided NetID doesn't exist
  - The student's logged status is FALSE

## API Endpoints

### Health Check

**Endpoint:** `GET /health`  
**Authentication Required:** No

Check API service availability.

**Response:**
```json
{
  "status": "healthy",
  "service": "yale-degree-audit"
}
```

### Degree Audit

**Endpoint:** `GET /api/degree-audit`  
**Authentication Required:** Yes

Check if a student has completed degree requirements. This performs a comprehensive audit of all requirements for all declared majors.

**Response:**
```json
{
  "status": "Not Completed",
  "unfulfilled_requirements": [
    {
      "major": "Computer Science",
      "requirement_name": "Core Requirements",
      "groups": [
        {
          "group_name": "Algorithms",
          "courses_completed": 0,
          "courses_required": 1,
          "courses_remaining": 1,
          "completed_courses": [],
          "available_courses": ["CPSC 365: Design and Analysis of Algorithms"]
        }
      ]
    }
  ]
}
```

### Majors

#### List All Majors

**Endpoint:** `GET /api/majors`  
**Authentication Required:** Yes

Retrieve a list of all available majors.

**Response:**
```json
[
  {
    "major_id": 101,
    "major_name": "Computer Science",
    "major_code": "CPSC",
    "department": "Department of Computer Science",
    "description": "The Computer Science major is designed to develop skills in all major areas of computer science while permitting flexibility in exploring particular areas of interest."
  }
]
```

#### Get Major Details

**Endpoint:** `GET /api/majors/{major_id}`  
**Authentication Required:** Yes

Get detailed information about a specific major.

**Response:**
```json
{
  "major_id": 101,
  "major_name": "Computer Science",
  "major_code": "CPSC",
  "department": "Department of Computer Science",
  "description": "The Computer Science major is designed to develop skills in all major areas of computer science while permitting flexibility in exploring particular areas of interest.",
  "latest_version": {
    "major_version_id": 201,
    "major_id": 101,
    "catalog_year": 2023,
    "effective_term": "Fall 2023",
    "valid_until_term": "Spring 2027",
    "is_active": true,
    "notes": "Updated CS curriculum with increased emphasis on AI and machine learning."
  }
}
```

#### Get Major Requirements

**Endpoint:** `GET /api/majors/{major_id}/requirements`  
**Authentication Required:** Yes

Get all requirements for a specific major.

**Query Parameters:**
- `catalog_year` (optional): Filter by catalog year (e.g., 2023)

**Response:**
```json
{
  "major_version": {
    "major_version_id": 201,
    "major_id": 101,
    "catalog_year": 2023,
    "effective_term": "Fall 2023",
    "valid_until_term": "Spring 2027",
    "is_active": true,
    "notes": "Updated CS curriculum with increased emphasis on AI and machine learning."
  },
  "requirements": [
    {
      "requirement_id": 801,
      "major_version_id": 201,
      "requirement_name": "Prerequisites",
      "requirement_type": "Prerequisite",
      "description": "Foundational courses required before declaring the CS major",
      "min_credits": 0,
      "max_credits": 0,
      "min_courses": 3,
      "max_courses": 3,
      "groups": [
        {
          "requirement_group_id": 901,
          "requirement_id": 801,
          "group_name": "Introductory Programming",
          "group_operator": "OR",
          "min_courses_in_group": 1,
          "max_courses_in_group": 1,
          "group_description": "Introductory programming requirement"
        }
      ]
    }
  ]
}
```

#### Get Major Courses

**Endpoint:** `GET /api/majors/{major_id}/courses`  
**Authentication Required:** Yes

Get all courses that can fulfill requirements for a specific major.

**Query Parameters:**
- `type` (optional): Filter by requirement type (e.g., "Core", "Prerequisite", "Elective")

**Response:**
```json
{
  "major_version": {
    "major_version_id": 201,
    "major_id": 101,
    "catalog_year": 2023,
    "effective_term": "Fall 2023",
    "valid_until_term": "Spring 2027",
    "is_active": true,
    "notes": "Updated CS curriculum with increased emphasis on AI and machine learning."
  },
  "courses": [
    {
      "course_id": 401,
      "subject_code": "CPSC",
      "course_number": "112",
      "course_title": "Introduction to Programming",
      "description": "An introduction to the concepts, techniques, and applications of computer programming and software development.",
      "credits": 1.0,
      "distribution": "QR"
    }
  ]
}
```

### Courses

#### List All Courses

**Endpoint:** `GET /api/courses`  
**Authentication Required:** Yes

Get a paginated list of all courses.

**Query Parameters:**
- `subject_code` (optional): Filter by subject code (e.g., "CPSC")
- `distribution` (optional): Filter by distribution requirement (e.g., "QR")
- `page` (optional): Page number for pagination (default: 1)
- `per_page` (optional): Number of courses per page (default: 50)

**Response:**
```json
{
  "page": 1,
  "per_page": 50,
  "total": 124,
  "courses": [
    {
      "course_id": 401,
      "subject_code": "CPSC",
      "course_number": "112",
      "course_title": "Introduction to Programming",
      "description": "An introduction to the concepts, techniques, and applications of computer programming and software development.",
      "credits": 1.0,
      "distribution": "QR"
    }
  ]
}
```

#### Get Course Details

**Endpoint:** `GET /api/courses/{course_id}`  
**Authentication Required:** Yes

Get detailed information about a specific course.

**Response:**
```json
{
  "course": {
    "course_id": 401,
    "subject_code": "CPSC",
    "course_number": "112",
    "course_title": "Introduction to Programming",
    "description": "An introduction to the concepts, techniques, and applications of computer programming and software development.",
    "credits": 1.0,
    "distribution": "QR"
  },
  "prerequisites": [
    {
      "course_id": 406,
      "prereq_course_id": 401,
      "concurrency_allowed": false,
      "prerequisite": {
        "course_id": 401,
        "subject_code": "CPSC",
        "course_number": "112",
        "course_title": "Introduction to Programming"
      }
    }
  ],
  "equivalents": []
}
```

#### Search Courses

**Endpoint:** `GET /api/courses/search`  
**Authentication Required:** Yes

Search for courses by title, subject code, or course number.

**Query Parameters:**
- `q` (required): Search query
- `limit` (optional): Maximum number of results (default: 10)

**Response:**
```json
[
  {
    "course_id": 408,
    "subject_code": "CPSC",
    "course_number": "365",
    "course_title": "Design and Analysis of Algorithms",
    "description": "Paradigms for algorithmic problem solving; algorithms and complexity.",
    "credits": 1.0,
    "distribution": "QR"
  }
]
```

#### Get Courses by Subject

**Endpoint:** `GET /api/courses/subject/{subject_code}`  
**Authentication Required:** Yes

Get all courses for a specific subject.

**Response:**
```json
[
  {
    "course_id": 401,
    "subject_code": "CPSC",
    "course_number": "112",
    "course_title": "Introduction to Programming",
    "description": "An introduction to the concepts, techniques, and applications of computer programming and software development.",
    "credits": 1.0,
    "distribution": "QR"
  }
]
```

#### Get Courses by Distribution

**Endpoint:** `GET /api/courses/distribution/{distribution}`  
**Authentication Required:** Yes

Get all courses that fulfill a specific distribution requirement.

**Response:**
```json
[
  {
    "course_id": 401,
    "subject_code": "CPSC",
    "course_number": "112",
    "course_title": "Introduction to Programming",
    "description": "An introduction to the concepts, techniques, and applications of computer programming and software development.",
    "credits": 1.0,
    "distribution": "QR"
  }
]
```

### Students

#### Get Student Information

**Endpoint:** `GET /api/students/{net_id}`  
**Authentication Required:** Yes

Get comprehensive information about a specific student.

**Response:**
```json
{
  "student": {
    "student_id": 1001,
    "net_id": "abc123",
    "first_name": "Alice",
    "last_name": "Brown",
    "class_year": 2026,
    "email": "alice.brown@yale.edu",
    "logged": true
  },
  "majors": [
    {
      "student_major_id": 301,
      "student_id": 1001,
      "major_version_id": 201,
      "declaration_date": "2023-05-15",
      "is_primary_major": true,
      "majorversions": {
        "major_version_id": 201,
        "major_id": 101,
        "catalog_year": 2023,
        "effective_term": "Fall 2023",
        "valid_until_term": "Spring 2027",
        "is_active": true,
        "notes": "Updated CS curriculum with increased emphasis on AI and machine learning.",
        "majors": {
          "major_id": 101,
          "major_name": "Computer Science",
          "major_code": "CPSC",
          "department": "Department of Computer Science",
          "description": "The Computer Science major is designed to develop skills in all major areas of computer science while permitting flexibility in exploring particular areas of interest."
        }
      }
    }
  ],
  "enrollments": [
    {
      "enrollment_id": 601,
      "student_id": 1001,
      "course_id": 401,
      "term_taken": "Fall 2022",
      "grade": "A",
      "status": "Completed",
      "course": {
        "course_id": 401,
        "subject_code": "CPSC",
        "course_number": "112",
        "course_title": "Introduction to Programming",
        "description": "An introduction to the concepts, techniques, and applications of computer programming and software development.",
        "credits": 1.0,
        "distribution": "QR"
      }
    }
  ],
  "plans": [
    {
      "plan_id": 701,
      "student_id": 1001,
      "course_id": 426,
      "intended_term": "Spring 2025",
      "priority": 1,
      "notes": "Interested in AI focus",
      "course": {
        "course_id": 426,
        "subject_code": "CPSC",
        "course_number": "483",
        "course_title": "Deep Learning",
        "description": "An introduction to deep neural networks and their applications.",
        "credits": 1.0,
        "distribution": "QR"
      }
    }
  ]
}
```

#### Get Student GPA

**Endpoint:** `GET /api/students/{net_id}/gpa`  
**Authentication Required:** Yes

Calculate the GPA for a student.

**Response:**
```json
{
  "student_id": 1001,
  "net_id": "abc123",
  "gpa": 3.85
}
```

### Student Course Management

#### Get Student Enrollments

**Endpoint:** `GET /api/student/courses/enrollments`  
**Authentication Required:** Yes

Get all course enrollments for the authenticated student.

**Query Parameters:**
- `status` (optional): Filter by enrollment status (e.g., "Completed", "Enrolled")

**Response:**
```json
[
  {
    "enrollment_id": 601,
    "student_id": 1001,
    "course_id": 401,
    "term_taken": "Fall 2022",
    "grade": "A",
    "status": "Completed",
    "course": {
      "course_id": 401,
      "subject_code": "CPSC",
      "course_number": "112",
      "course_title": "Introduction to Programming",
      "description": "An introduction to the concepts, techniques, and applications of computer programming and software development.",
      "credits": 1.0,
      "distribution": "QR"
    }
  }
]
```

#### Add Course Enrollment

**Endpoint:** `POST /api/student/courses/enrollments`  
**Authentication Required:** Yes

Add a new course enrollment for the authenticated student.

**Request Body:**
```json
{
  "course_id": 408,
  "term_taken": "Fall 2024",
  "grade": "B+",
  "status": "Completed"
}
```

**Response:**
```json
{
  "enrollment_id": 645,
  "student_id": 1001,
  "course_id": 408,
  "term_taken": "Fall 2024",
  "grade": "B+",
  "status": "Completed",
  "course": {
    "course_id": 408,
    "subject_code": "CPSC",
    "course_number": "365",
    "course_title": "Design and Analysis of Algorithms",
    "description": "Paradigms for algorithmic problem solving; algorithms and complexity.",
    "credits": 1.0,
    "distribution": "QR"
  }
}
```

#### Update Course Enrollment

**Endpoint:** `PUT /api/student/courses/enrollments/{enrollment_id}`  
**Authentication Required:** Yes

Update an existing course enrollment for the authenticated student.

**Request Body:**
```json
{
  "grade": "A-",
  "status": "Completed"
}
```

**Response:**
```json
{
  "enrollment_id": 645,
  "student_id": 1001,
  "course_id": 408,
  "term_taken": "Fall 2024",
  "grade": "A-",
  "status": "Completed",
  "course": {
    "course_id": 408,
    "subject_code": "CPSC",
    "course_number": "365",
    "course_title": "Design and Analysis of Algorithms",
    "description": "Paradigms for algorithmic problem solving; algorithms and complexity.",
    "credits": 1.0,
    "distribution": "QR"
  }
}
```

#### Delete Course Enrollment

**Endpoint:** `DELETE /api/student/courses/enrollments/{enrollment_id}`  
**Authentication Required:** Yes

Delete a course enrollment for the authenticated student.

**Response:**
```json
{
  "message": "Enrollment deleted successfully",
  "enrollment_id": 645
}
```

#### Get Course Plans

**Endpoint:** `GET /api/student/courses/plans`  
**Authentication Required:** Yes

Get all course plans for the authenticated student.

**Response:**
```json
[
  {
    "plan_id": 701,
    "student_id": 1001,
    "course_id": 426,
    "intended_term": "Spring 2025",
    "priority": 1,
    "notes": "Interested in AI focus",
    "course": {
      "course_id": 426,
      "subject_code": "CPSC",
      "course_number": "483",
      "course_title": "Deep Learning",
      "description": "An introduction to deep neural networks and their applications.",
      "credits": 1.0,
      "distribution": "QR"
    }
  }
]
```

#### Add Course Plan

**Endpoint:** `POST /api/student/courses/plans`  
**Authentication Required:** Yes

Add a new course plan for the authenticated student.

**Request Body:**
```json
{
  "course_id": 419,
  "intended_term": "Fall 2025",
  "priority": 2,
  "notes": "Interested in big data systems"
}
```

**Response:**
```json
{
  "plan_id": 715,
  "student_id": 1001,
  "course_id": 419,
  "intended_term": "Fall 2025",
  "priority": 2,
  "notes": "Interested in big data systems",
  "course": {
    "course_id": 419,
    "subject_code": "CPSC",
    "course_number": "436",
    "course_title": "Big Data Systems",
    "description": "Design of systems for storing and processing large-scale data.",
    "credits": 1.0,
    "distribution": "QR"
  }
}
```

#### Update Course Plan

**Endpoint:** `PUT /api/student/courses/plans/{plan_id}`  
**Authentication Required:** Yes

Update an existing course plan for the authenticated student.

**Request Body:**
```json
{
  "intended_term": "Spring 2026",
  "priority": 1
}
```

**Response:**
```json
{
  "plan_id": 715,
  "student_id": 1001,
  "course_id": 419,
  "intended_term": "Spring 2026",
  "priority": 1,
  "notes": "Interested in big data systems",
  "course": {
    "course_id": 419,
    "subject_code": "CPSC",
    "course_number": "436",
    "course_title": "Big Data Systems",
    "description": "Design of systems for storing and processing large-scale data.",
    "credits": 1.0,
    "distribution": "QR"
  }
}
```

#### Delete Course Plan

**Endpoint:** `DELETE /api/student/courses/plans/{plan_id}`  
**Authentication Required:** Yes

Delete a course plan for the authenticated student.

**Response:**
```json
{
  "message": "Course plan deleted successfully",
  "plan_id": 715
}
```

#### Batch Add Enrollments

**Endpoint:** `POST /api/student/courses/batch/add-enrollments`  
**Authentication Required:** Yes

Add multiple course enrollments for the authenticated student in a single request.

**Request Body:**
```json
{
  "enrollments": [
    {
      "course_id": 408,
      "term_taken": "Fall 2024",
      "grade": "B+",
      "status": "Completed"
    },
    {
      "course_id": 409,
      "term_taken": "Fall 2024",
      "grade": "A-",
      "status": "Completed"
    }
  ]
}
```

**Response:**
```json
{
  "message": "Successfully added 2 enrollments",
  "enrollments": [
    {
      "enrollment_id": 645,
      "student_id": 1001,
      "course_id": 408,
      "term_taken": "Fall 2024",
      "grade": "B+",
      "status": "Completed",
      "course": {
        "course_id": 408,
        "subject_code": "CPSC",
        "course_number": "365",
        "course_title": "Design and Analysis of Algorithms",
        "description": "Paradigms for algorithmic problem solving; algorithms and complexity.",
        "credits": 1.0,
        "distribution": "QR"
      }
    },
    {
      "enrollment_id": 646,
      "student_id": 1001,
      "course_id": 409,
      "term_taken": "Fall 2024",
      "grade": "A-",
      "status": "Completed",
      "course": {
        "course_id": 409,
        "subject_code": "CPSC",
        "course_number": "366",
        "course_title": "Intensive Algorithms",
        "description": "A rigorous introduction to the design and analysis of efficient algorithms.",
        "credits": 1.0,
        "distribution": "QR"
      }
    }
  ]
}
```

#### Batch Delete Enrollments

**Endpoint:** `POST /api/student/courses/batch/delete-enrollments`  
**Authentication Required:** Yes

Delete multiple course enrollments for the authenticated student in a single request.

**Request Body:**
```json
{
  "enrollment_ids": [645, 646]
}
```

**Response:**
```json
{
  "message": "Successfully deleted 2 enrollments",
  "deleted_ids": [645, 646],
  "not_found_ids": []
}
```

## Response Codes

| Code | Description |
|------|-------------|
| 200  | OK - The request was successful |
| 201  | Created - A new resource was successfully created |
| 400  | Bad Request - The request was invalid or cannot be otherwise served |
| 401  | Unauthorized - Authentication is required or failed |
| 404  | Not Found - The requested resource was not found |
| 405  | Method Not Allowed - The HTTP method is not supported for this resource |
| 500  | Server Error - An internal server error occurred |

## Security Features

1. **Global Authentication**: All endpoints (except `/health`) require authentication via the X-Student-NetID header
2. **Login Status Verification**: Student login status is verified in the database before allowing access
3. **CORS Support**: Proper CORS headers implemented for cross-origin requests
4. **Error Handling**: Comprehensive error handling for all request scenarios
5. **Input Validation**: Request validation using Pydantic models

## Architecture Features

1. **Layered Architecture**:
   - Models (Schemas): Data validation and type checking using Pydantic
   - Repositories: Database access and CRUD operations
   - Services: Business logic and orchestration
   - API Routes: HTTP interface and request handling

2. **Database Integration**: Uses Supabase for data storage and retrieval

3. **Codebase Organization**:
   - Modular file structure
   - Clear separation of concerns
   - Consistent naming conventions
   - Blueprint-based route organization

## API Versioning

The current version is v1 (implicitly). Future versions will be explicitly versioned in the URL path (e.g., `/api/v2/...`).

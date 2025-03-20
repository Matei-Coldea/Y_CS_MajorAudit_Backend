# Yale Degree Audit System

A Flask-based REST API for checking degree completion and managing degree audit data for Yale University academic programs.

## Authentication

All endpoints (except `/health`) require authentication via the `X-Student-NetID` header. The server validates that:
1. The header is present in the request
2. The NetID exists in the database
3. The student is logged in (has an active session)

Example request:
```bash
curl -X GET \
  'http://localhost:5000/api/student' \
  -H 'X-Student-NetID: abc123'
```

Failed authentication will result in one of these responses:
- Missing header: 401 Unauthorized with message "Authentication required"
- Invalid NetID: 401 Unauthorized with message "User not found"
- User not logged in: 401 Unauthorized with message "User is not logged in"

## Architecture

The application follows a layered architecture with clear separation of concerns:

### Layers

1. **Models (Schemas)**
   - Implemented using Pydantic
   - Data validation and type checking
   - API contract definition

2. **Repositories**
   - Database access abstraction
   - CRUD operations
   - Query building

3. **Services**
   - Business logic encapsulation
   - Coordination between repositories
   - Complex operations

4. **API Routes**
   - HTTP request handling
   - Input validation
   - Response formatting

### Project Structure

```
yale-degree-audit/
├── app.py                     # Application entry point
├── config.py                  # Configuration handling
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── requirements.txt           # Dependencies
├── .env.example               # Environment variable example
│
├── api/                       # API routes
│   ├── __init__.py
│   ├── degree_audit.py        # Degree audit endpoints (/api/degree-audit)
│   ├── majors.py              # Major-related endpoints (/api/major/*)
│   ├── courses.py             # Course-related endpoints (/api/course/*)
│   ├── students.py            # Student-related endpoints (/api/student/*)
│   └── distributions.py       # Distribution requirements endpoints (/api/distribution-requirement/*)
│
├── models/                    # Pydantic models (schemas)
│   ├── __init__.py
│   ├── course.py              # Course-related schemas
│   ├── degree_audit.py        # Degree audit schemas
│   ├── major.py               # Major-related schemas
│   └── student.py             # Student-related schemas
│
├── repositories/              # Database access layer
│   ├── __init__.py
│   ├── base.py                # Base repository class
│   ├── course_repository.py   # Course data access
│   ├── major_repository.py    # Major data access
│   ├── student_repository.py  # Student data access
│   └── distribution_repository.py # Distribution requirements data access
│
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── course_service.py      # Course-related logic
│   ├── degree_audit_service.py # Degree audit logic
│   ├── major_service.py       # Major-related logic
│   ├── student_service.py     # Student-related logic
│   └── distribution_service.py # Distribution requirements logic
│
└── utils/                     # Utility functions
    ├── __init__.py
    ├── grade_utils.py         # Grade calculation utilities
    └── auth.py               # Authentication utilities
```

## API Endpoints

### Health Check

- `GET /health` - Check if the service is running
  - No authentication required
  - Returns service status and name
  
  Example response:
  ```json
  {
    "status": "healthy",
    "service": "Yale Degree Audit API",
    "version": "1.0.0"
  }
  ```

### Degree Audit

- `GET /api/degree-audit` - Check if a student has completed their major requirements
  - **Required Header**: `X-Student-NetID`
  - Returns completion status and unfulfilled requirements
  
  Example response for student 'abc123' (Computer Science major):
  ```json
  {
    "student_id": "abc123",
    "major": {
      "name": "Computer Science",
      "requirements": {
        "prerequisites": {
          "completed": true,
          "courses": ["CPSC 112", "CPSC 201", "MATH 112"]
        },
        "core": {
          "completed": false,
          "courses": {
            "completed": ["CPSC 223", "CPSC 323"],
            "remaining": ["CPSC 365"]
          }
        },
        "electives": {
          "completed": false,
          "courses": {
            "completed": ["CPSC 419"],
            "remaining_count": 5
          }
        }
      }
    },
    "distribution_requirements": {
      "year": "Sophomore",
      "status": "In Progress",
      "details": {
        "skills": {
          "QR": {"required": 2, "completed": 2},
          "WR": {"required": 2, "completed": 1},
          "L": {"required": 1, "completed": 0}
        },
        "disciplinary": {
          "Hu": {"required": 2, "completed": 1},
          "Sc": {"required": 2, "completed": 2},
          "So": {"required": 2, "completed": 1}
        }
      }
    }
  }
  ```

### Distribution Requirements

- `GET /api/distribution-requirement` - Get a student's overall distribution requirements status
  - **Required Header**: `X-Student-NetID`
  
  Example response for student 'abc123':
  ```json
  {
    "student_id": "abc123",
    "current_year": "Sophomore",
    "overall_status": {
      "skills": {
        "QR": {
          "required": 2,
          "completed": 2,
          "courses": ["CPSC 112", "MATH 112"]
        },
        "WR": {
          "required": 2,
          "completed": 1,
          "courses": ["ENGL 114"]
        },
        "L": {
          "required": 1,
          "completed": 0,
          "courses": []
        }
      },
      "disciplinary": {
        "Hu": {
          "required": 2,
          "completed": 1,
          "courses": ["ENGL 115"]
        },
        "Sc": {
          "required": 2,
          "completed": 2,
          "courses": ["CPSC 201", "CPSC 223"]
        },
        "So": {
          "required": 2,
          "completed": 1,
          "courses": ["PLSC 101"]
        }
      }
    }
  }
  ```

- `GET /api/distribution-requirement/{year}` - Get requirements for a specific year
  - **Required Header**: `X-Student-NetID`
  
  Example response for student 'abc123', year 'Freshman':
  ```json
  {
    "student_id": "abc123",
    "year": "Freshman",
    "requirements": {
      "rule": "Complete courses in 2 of 3 skills categories",
      "progress": {
        "QR": {
          "required": 1,
          "completed": 1,
          "courses": ["CPSC 112"]
        },
        "WR": {
          "required": 1,
          "completed": 1,
          "courses": ["ENGL 114"]
        },
        "L": {
          "required": 1,
          "completed": 0,
          "courses": []
        }
      },
      "status": "Completed",
      "details": "Completed 2 of 3 required skills categories (QR, WR)"
    }
  }
  ```

### Majors

- `GET /api/major` - Get all available majors
  - **Required Header**: `X-Student-NetID`
  
  Example response:
  ```json
  {
    "majors": [
      {
        "major_id": 101,
        "major_name": "Computer Science",
        "major_code": "CPSC",
        "department": "Department of Computer Science",
        "description": "The Computer Science major is designed to develop skills in all major areas of computer science while permitting flexibility in exploring particular areas of interest."
      },
      {
        "major_id": 102,
        "major_name": "English Language and Literature",
        "major_code": "ENGL",
        "department": "Department of English",
        "description": "The English major offers a rich and diverse curriculum exploring the history of literature written in English and introducing students to a variety of methods for critical analysis and interpretation."
      }
    ]
  }
  ```

- `GET /api/major/{major_id}/requirements` - Get major requirements
  - **Required Header**: `X-Student-NetID`
  
  Example response for Computer Science (major_id: 101):
  ```json
  {
    "major_name": "Computer Science",
    "catalog_year": 2023,
    "requirements": {
      "prerequisites": {
        "name": "Prerequisites",
        "courses": [
          {
            "code": "CPSC 112",
            "name": "Introduction to Programming"
          },
          {
            "code": "CPSC 201",
            "name": "Introduction to Computer Science"
          },
          {
            "code": "MATH 112",
            "name": "Calculus I"
          }
        ]
      },
      "core": {
        "name": "Core Requirements",
        "courses": [
          {
            "code": "CPSC 223",
            "name": "Data Structures and Programming Techniques"
          },
          {
            "code": "CPSC 323",
            "name": "Systems Programming and Computer Organization"
          },
          {
            "code": "CPSC 365",
            "name": "Design and Analysis of Algorithms"
          }
        ]
      },
      "electives": {
        "name": "Advanced Electives",
        "min_courses": 6,
        "rules": [
          "At least 4 courses must be at 400-level or above",
          "At least one theory course is required"
        ]
      }
    }
  }
  ```

### Courses

- `GET /api/course` - Get list of courses
  - **Required Header**: `X-Student-NetID`
  
  Example response:
  ```json
  {
    "page": 1,
    "per_page": 2,
    "total": 24,
    "courses": [
      {
        "course_id": 401,
        "subject_code": "CPSC",
        "course_number": "112",
        "course_title": "Introduction to Programming",
        "description": "An introduction to the concepts, techniques, and applications of computer programming and software development.",
        "credits": 1.0,
        "distribution": "QR"
      },
      {
        "course_id": 402,
        "subject_code": "CPSC",
        "course_number": "201",
        "course_title": "Introduction to Computer Science",
        "description": "Introduction to the concepts and techniques of computer science.",
        "credits": 1.0,
        "distribution": "QR"
      }
    ]
  }
  ```

- `GET /api/course/{course_id}` - Get course details
  - **Required Header**: `X-Student-NetID`
  
  Example response for CPSC 223 (course_id: 406):
  ```json
  {
    "course_id": 406,
    "subject_code": "CPSC",
    "course_number": "223",
    "course_title": "Data Structures and Programming Techniques",
    "description": "Organization of data, algorithms, techniques, and classes.",
    "credits": 1.0,
    "distribution": "QR",
    "prerequisites": [
      {
        "course_id": 401,
        "code": "CPSC 112",
        "title": "Introduction to Programming"
      },
      {
        "course_id": 402,
        "code": "CPSC 201",
        "title": "Introduction to Computer Science"
      }
    ]
  }
  ```

### Students

- `GET /api/student` - Get student information
  - **Required Header**: `X-Student-NetID`
  
  Example response for 'abc123':
  ```json
  {
    "student_id": 1001,
    "net_id": "abc123",
    "first_name": "Alice",
    "last_name": "Brown",
    "class_year": 2026,
    "email": "alice.brown@yale.edu",
    "majors": [
      {
        "major_name": "Computer Science",
        "is_primary": true,
        "declaration_date": "2023-05-15"
      }
    ]
  }
  ```

- `GET /api/student/enrollments` - Get student's course enrollments
  - **Required Header**: `X-Student-NetID`
  
  Example response for 'abc123':
  ```json
  {
    "student_id": "abc123",
    "enrollments": {
      "completed": [
        {
          "course_code": "CPSC 112",
          "title": "Introduction to Programming",
          "term": "Fall 2022",
          "grade": "A",
          "credits": 1.0
        },
        {
          "course_code": "MATH 112",
          "title": "Calculus I",
          "term": "Fall 2022",
          "grade": "A-",
          "credits": 1.0
        }
      ],
      "current": [
        {
          "course_code": "CPSC 414",
          "title": "Web Programming",
          "term": "Fall 2024",
          "status": "Enrolled"
        },
        {
          "course_code": "CPSC 408",
          "title": "Algorithms",
          "term": "Fall 2024",
          "status": "Enrolled"
        }
      ]
    }
  }
  ```

- `GET /api/student/gpa` - Get student's GPA
  - **Required Header**: `X-Student-NetID`
  
  Example response for 'abc123':
  ```json
  {
    "student_id": "abc123",
    "overall_gpa": 3.83,
    "by_term": [
      {
        "term": "Fall 2022",
        "gpa": 4.0,
        "credits": 2.0
      },
      {
        "term": "Spring 2023",
        "gpa": 3.67,
        "credits": 2.0
      }
    ]
  }
  ```

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- Supabase account and project

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yale-degree-audit.git
   cd yale-degree-audit
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file with your Supabase credentials and other configuration

5. Run the application:
   ```bash
   python app.py
   ```

### Running with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yale-degree-audit.git
   cd yale-degree-audit
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your Supabase credentials and other configuration

4. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

5. Access the API at http://localhost:5000

## Database Schema

The application uses a PostgreSQL database with the following structure:

https://docs.google.com/document/d/1NB3KsjMmYX4DS3ibNFB1wk3rresBxfEMYK4Wrq08TBw/edit?tab=t.0
https://docs.google.com/document/d/1ZIA1XXF8_w1Nh0yC7caXWX4dWAY3P1PXAfbwgTO5NHo/edit?tab=t.0

### Core Student Data

**Students**
- Primary table for student information
- Fields:
  - `student_id` (PK): Unique identifier
  - `net_id`: Yale NetID (unique)
  - `first_name`, `last_name`: Student's name
  - `class_year`: Expected graduation year
  - `email`: Yale email address
- Used for authentication and basic student information

### Major-Related Tables

**Majors**
- Defines available majors at Yale
- Fields:
  - `major_id` (PK): Unique identifier
  - `major_name`: Full name of the major
  - `major_code`: Department code (e.g., "CPSC")
  - `department`: Department name
  - `description`: Detailed major description

**MajorVersions**
- Tracks different versions of major requirements over time
- Fields:
  - `major_version_id` (PK): Unique identifier
  - `major_id` (FK): References Majors
  - `catalog_year`: Academic year of this version
  - `effective_term`, `valid_until_term`: Validity period
  - `is_active`: Whether this version is current
  - `notes`: Changes or special considerations

**StudentMajors**
- Links students to their declared majors
- Fields:
  - `student_major_id` (PK): Unique identifier
  - `student_id` (FK): References Students
  - `major_version_id` (FK): References MajorVersions
  - `declaration_date`: When the major was declared
  - `is_primary_major`: Boolean for primary/secondary status

### Course-Related Tables

**Courses**
- Comprehensive course catalog
- Fields:
  - `course_id` (PK): Unique identifier
  - `subject_code`: Department code
  - `course_number`: Course number within department
  - `course_title`: Full course name
  - `description`: Course description
  - `credits`: Number of credits
  - `distribution`: Distribution requirement codes

**StudentCourseEnrollments**
- Tracks completed and current courses
- Fields:
  - `enrollment_id` (PK): Unique identifier
  - `student_id` (FK): References Students
  - `course_id` (FK): References Courses
  - `term_taken`: Academic term
  - `grade`: Course grade
  - `status`: 'Completed', 'Enrolled', or 'Withdrawn'

**StudentCoursePlans**
- Future course planning
- Fields:
  - `plan_id` (PK): Unique identifier
  - `student_id` (FK): References Students
  - `course_id` (FK): References Courses
  - `intended_term`: Planned term
  - `priority`: Student's priority level
  - `notes`: Planning notes

### Requirement Structure

**MajorRequirements**
- Top-level requirements for each major
- Fields:
  - `requirement_id` (PK): Unique identifier
  - `major_version_id` (FK): References MajorVersions
  - `requirement_name`: Name of requirement
  - `requirement_type`: 'Prerequisite', 'Core', 'Elective', or 'Capstone'
  - `min_courses`, `max_courses`: Course count limits
  - `min_credits`, `max_credits`: Credit limits

**RequirementGroups**
- Subdivides requirements into specific groups
- Fields:
  - `requirement_group_id` (PK): Unique identifier
  - `requirement_id` (FK): References MajorRequirements
  - `group_name`: Name of the group
  - `group_operator`: 'AND' or 'OR'
  - `min_courses_in_group`, `max_courses_in_group`: Course limits
  - `group_description`: Detailed description

**RequirementGroupCourses**
- Maps courses to requirement groups
- Fields:
  - `req_group_course_id` (PK): Unique identifier
  - `requirement_group_id` (FK): References RequirementGroups
  - `course_id` (FK): References Courses
  - `is_required_in_group`: Whether course is mandatory

### Course Relationships

**CoursePrerequisites**
- Defines prerequisite relationships
- Fields:
  - `course_id` (FK): The main course
  - `prereq_course_id` (FK): The prerequisite course
  - `concurrency_allowed`: Can be taken simultaneously

**EquivalenceGroups**
- Defines groups of equivalent courses
- Fields:
  - `eq_group_id` (PK): Unique identifier
  - `group_name`: Name of the equivalence group
  - `group_notes`: Additional information

**EquivalenceGroupCourses**
- Maps courses to equivalence groups
- Fields:
  - `eq_group_course_id` (PK): Unique identifier
  - `eq_group_id` (FK): References EquivalenceGroups
  - `course_id` (FK): References Courses

### Distribution Requirements

**DistributionTypes**
- Defines types of distribution requirements
- Fields:
  - `distribution_id` (PK): Unique identifier
  - `code`: Short code (e.g., "QR", "WR")
  - `name`: Full name
  - `description`: Detailed description
  - `category`: Either 'skills' or 'disciplinary'

**AcademicYears**
- Defines the four academic years
- Fields:
  - `year_id` (PK): Unique identifier
  - `name`: Year name (e.g., "Freshman")
  - `display_order`: Ordering (1-4)
  - `description`: Year-specific information

**DistributionRequirements**
- Maps requirements to academic years
- Fields:
  - `requirement_id` (PK): Unique identifier
  - `year_id` (FK): References AcademicYears
  - `distribution_id` (FK): References DistributionTypes
  - `courses_required`: Number of courses needed
  - `active`: Whether requirement is current
  - `created_at`, `updated_at`: Timestamps

**YearRequirementRules**
- Special rules for distribution requirements
- Fields:
  - `rule_id` (PK): Unique identifier
  - `year_id` (FK): References AcademicYears
  - `rule_type`: Type of rule
  - `value`: Numeric requirement
  - `category`: Applies to 'skills' or 'disciplinary'
  - `active`: Whether rule is current

### Database Features

- **Foreign Key Constraints**: Ensure referential integrity between tables
- **Unique Constraints**: Prevent duplicate entries (e.g., NetIDs)
- **Check Constraints**: Validate data (e.g., grade values)
- **Default Values**: Automatic timestamps and boolean flags
- **Indexes**: Optimized for common queries and joins

## Development

### Adding New Features

1. Cacheing
2. Better login checking (just querying supabase table for login is not safe)





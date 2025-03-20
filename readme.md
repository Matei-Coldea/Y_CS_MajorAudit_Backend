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
  'http://localhost:5000/api/students/abc123' \
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
│   ├── degree_audit.py        # Degree audit endpoints
│   ├── majors.py              # Major-related endpoints
│   ├── courses.py             # Course-related endpoints
│   ├── students.py            # Student-related endpoints
│   └── distributions.py       # Distribution requirements endpoints
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

### Degree Audit

- `GET /api/degree-audit` - Check if a student has completed their major requirements
  - **Required Header**: `X-Student-NetID`
  - Returns completion status and unfulfilled requirements

### Distribution Requirements

- `GET /api/distribution-requirements/{net_id}` - Get a student's overall distribution requirements status
  - **Required Header**: `X-Student-NetID`
  - Returns:
    - Current year and fulfillment status
    - Progress for each distribution category
    - Year-specific requirements and completion status
    - Total distribution requirements for graduation

- `GET /api/distribution-requirements/{net_id}/{year}` - Get a student's distribution requirements for a specific year
  - **Required Header**: `X-Student-NetID`
  - Year must be one of: "Freshman", "Sophomore", "Junior", "Senior"
  - Returns detailed status for the specified academic year

### Majors

- `GET /api/majors` - Get a list of all available majors
  - **Required Header**: `X-Student-NetID`
- `GET /api/majors/{major_id}` - Get detailed information about a specific major
  - **Required Header**: `X-Student-NetID`
- `GET /api/majors/{major_id}/requirements` - Get all requirements for a specific major
  - **Required Header**: `X-Student-NetID`
  - Optional `catalog_year` query parameter
- `GET /api/majors/{major_id}/courses` - Get all courses that can fulfill requirements for a specific major
  - **Required Header**: `X-Student-NetID`
  - Optional `type` query parameter to filter by requirement type

### Courses

- `GET /api/courses` - Get a list of all courses with optional filtering
  - **Required Header**: `X-Student-NetID`
  - Optional `subject_code` and `distribution` query parameters
  - Pagination with `page` and `per_page` parameters
- `GET /api/courses/{course_id}` - Get detailed information about a specific course
  - **Required Header**: `X-Student-NetID`
- `GET /api/courses/search` - Search for courses by title, subject code, or course number
  - **Required Header**: `X-Student-NetID`
  - Required `q` query parameter
  - Optional `limit` parameter
- `GET /api/courses/subject/{subject_code}` - Get all courses for a specific subject
  - **Required Header**: `X-Student-NetID`
- `GET /api/courses/distribution/{distribution}` - Get all courses that fulfill a specific distribution requirement
  - **Required Header**: `X-Student-NetID`

### Students

- `GET /api/students/{net_id}` - Get information about a specific student
  - **Required Header**: `X-Student-NetID`
- `GET /api/students/{net_id}/enrollments` - Get all course enrollments for a student
  - **Required Header**: `X-Student-NetID`
  - Optional `status` query parameter
- `GET /api/students/{net_id}/gpa` - Calculate the GPA for a student
  - **Required Header**: `X-Student-NetID`

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

The application uses the following database tables:

- Students - Core data about each Yale student
- Majors - High-level table for each major offered
- MajorVersions - Allows multiple versions of a major
- StudentMajors - Links a student to a specific version of a major
- Courses - Catalog of Yale courses
- StudentCourseEnrollments - Which students took which courses
- StudentCoursePlans - Lets students plan future courses
- MajorRequirements - Top-level requirements for majors
- RequirementGroups - Subdivide requirements into groups
- RequirementGroupCourses - Maps groups to courses
- RequirementRules - For advanced logic requirements
- CoursePrerequisites - Tracks prerequisites for courses
- EquivalenceGroups - Defines clusters of equivalent courses

New tables for distribution requirements:

- **DistributionTypes** - Defines different types of distribution requirements
  - Categories: Skills (QR, WR, L) and Disciplinary (Hu, Sc, So)
  - Tracks name, code, and description

- **AcademicYears** - Defines the four academic years and their requirements
  - Tracks year name, display order, and description

- **DistributionRequirements** - Maps requirements to academic years
  - Specifies number of courses required for each distribution type per year
  - Tracks active status and timestamps

- **YearRequirementRules** - Defines special rules for each year
  - Examples: "2 of 3 skills categories for Freshman"
  - Supports different rule types and categories

Refer to the ERD documentation for more details on the database schema.

## Development

### Adding New Features

1. Cacheing





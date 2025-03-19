# Yale Degree Audit System

A Flask-based REST API for checking degree completion and managing degree audit data for Yale University academic programs.

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
│   └── students.py            # Student-related endpoints
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
│   └── student_repository.py  # Student data access
│
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── course_service.py      # Course-related logic
│   ├── degree_audit_service.py # Degree audit logic
│   ├── major_service.py       # Major-related logic
│   └── student_service.py     # Student-related logic
│
└── utils/                     # Utility functions
    ├── __init__.py
    └── grade_utils.py         # Grade calculation utilities
```

## API Endpoints

### Degree Audit

- `GET /api/degree-audit` - Check if a student has completed their major requirements
  - Requires `X-Student-NetID` header
  - Returns completion status and unfulfilled requirements

### Majors

- `GET /api/majors` - Get a list of all available majors
- `GET /api/majors/{major_id}` - Get detailed information about a specific major
- `GET /api/majors/{major_id}/requirements` - Get all requirements for a specific major
  - Optional `catalog_year` query parameter
- `GET /api/majors/{major_id}/courses` - Get all courses that can fulfill requirements for a specific major
  - Optional `type` query parameter to filter by requirement type

### Courses

- `GET /api/courses` - Get a list of all courses with optional filtering
  - Optional `subject_code` and `distribution` query parameters
  - Pagination with `page` and `per_page` parameters
- `GET /api/courses/{course_id}` - Get detailed information about a specific course
- `GET /api/courses/search` - Search for courses by title, subject code, or course number
  - Required `q` query parameter
  - Optional `limit` parameter
- `GET /api/courses/subject/{subject_code}` - Get all courses for a specific subject
- `GET /api/courses/distribution/{distribution}` - Get all courses that fulfill a specific distribution requirement

### Students

- `GET /api/students/{net_id}` - Get information about a specific student
- `GET /api/students/{net_id}/enrollments` - Get all course enrollments for a student
  - Optional `status` query parameter
- `GET /api/students/{net_id}/gpa` - Calculate the GPA for a student

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

Refer to the ERD documentation for more details on the database schema.

## Development

### Adding New Features

1. Create appropriate Pydantic models in the `models/` directory
2. Add repository methods in the relevant repository class
3. Implement business logic in the service layer
4. Create API routes in the appropriate blueprint file
5. Register any new blueprints in `api/__init__.py`

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting
- Type annotations for better IDE support

## License

[MIT License](LICENSE)


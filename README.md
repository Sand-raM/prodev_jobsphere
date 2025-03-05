# JobSphere - Job Board Backend

## Overview
JobSphere is a backend system for a Job Board Platform, enabling users to post jobs, apply for positions, and manage applications efficiently. The system features role-based access control, optimized database queries, and comprehensive API documentation.

## Project Goals
The primary objectives of the JobSphere backend are:
- **API Development**: Build APIs for managing job postings, categories, and applications.
- **Access Control**: Implement role-based access control for admins, staff, and users.
- **Database Efficiency**: Optimize job search with advanced query indexing.

## Technologies Used
| Technology   | Purpose |
|-------------|---------|
| Django      | High-level Python framework for rapid development |
| Django REST Framework | API development and authentication |
| PostgreSQL  | Database for storing job board data |
| JWT         | Secure role-based authentication |
| Swagger     | API endpoint documentation |
| Docker      | Containerization for scalable deployment |
| Redis       | Caching frequently accessed data |

## Key Features
### 1. Job Posting Management
- APIs for creating, updating, deleting, and retrieving job postings.
- Jobs categorized by industry, location, and type.

### 2. Role-Based Authentication
- Admins can manage jobs and categories.
- Staff members can post jobs.
- Regular users can apply for jobs and manage applications.

### 3. Optimized Job Search
- Indexing and optimized queries for efficient job filtering.
- Location-based and category-based filtering.

### 4. Application Management
- Users can submit applications with a cover letter and resume.
- Applications are stored and retrieved efficiently.

### 5. API Documentation
- Swagger documentation is hosted at `/api/docs` for frontend integration.

## Installation
### Prerequisites
- Python 3.9+
- PostgreSQL
- Docker (optional for containerized setup)

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sand-raM/prodev_jobsphere.git
   cd jobsphere
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/jobs/` | GET | Retrieve job listings |
| `/api/jobs/` | POST | Create a new job (Admin/Staff only) |
| `/api/jobs/{id}/` | PUT | Update a job (Admin/Staff only) |
| `/api/jobs/{id}/` | DELETE | Delete a job (Admin only) |
| `/api/applications/` | GET | List all applications (Authenticated users) |
| `/api/applications/` | POST | Apply for a job |
| `/api/auth/login/` | POST | User authentication |
| `/api/auth/register/` | POST | User registration |
| `/api/docs/` | GET | Access API documentation |

## Git Commit Workflow
| Commit Type | Example |
|-------------|---------|
| **Initial Setup** | `feat: set up Django project with PostgreSQL` |
| **Feature Development** | `feat: implement job posting and filtering APIs` |
| **Optimization** | `perf: optimize job search queries with indexing` |
| **Documentation** | `docs: update README with usage details` |

## Deployment
- The API and Swagger documentation should be deployed and hosted for public access.
- Use Docker for scalable deployment.
- Consider integrating CI/CD for automated testing and deployment.

## Evaluation Criteria
| Criteria | Details |
|----------|---------|
| **Functionality** | APIs handle job and application CRUD operations effectively. Role-based authentication works as intended. |
| **Code Quality** | Code is modular and follows Django best practices. Database schema is normalized and efficient. |
| **Performance** | Job search is optimized and responsive. Indexed queries enhance filtering efficiency. |
| **Documentation** | Swagger documentation is hosted and well-structured. README provides clear setup instructions. |

---
### Contributors
- **Sandra MURAZA** - Backend Developer

For more details, visit the [GitHub repository](https://github.com/Sand-raM/prodev_jobsphere).


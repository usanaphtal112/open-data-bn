# DiversedataHub Backend

The backend of **DiversedataHub** is built using **Django REST Framework (DRF)**, offering a scalable RESTful API to manage diverse data categories, including Education, Health, Restaurants, Hotels, Beauty Spas, Home Décor, and more.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites
Ensure you have the following installed before proceeding:
- **Python** (v3.10 or higher)
- **Pip** (Python package manager)
- **PostgreSQL** (as the database engine)
- **Git** (for version control)

## Installation
1. Clone the repository:
   ```bash
   https://github.com/usanaphtal112/open-data-bn
   cd open-data-bn
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```
3. Install required dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Running the Application
1. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```
   The API will be accessible at `http://localhost:8000/api/v1/`.

## Project Structure
```
diversedatahub-backend/
    ├── accounts/                    # User authentication and management
    ├── healthdata/                  # Health facility data management
    ├── edudata/                     # Educational institution data management
    ├── core/                        # Project-wide utilities and configurations
    ├── media/                       # Media file storage
    ├── static/                      # Static assets (CSS, JS, images)
    ├── .gitignore                   # Git ignore file
    ├── manage.py                    # Django management script
    ├── .env                         # Environment variables
    ├── requirements.txt             # Project dependencies
    ├── Dockerfile                   # Docker containerization setup
    └── README.md
```

## API Documentation
Interactive API documentation is available at:
- **Swagger UI**: [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)
- **ReDoc**: [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)

## Database Setup
This project uses **PostgreSQL**. Configure the database settings in `settings.py`:

```python
    from decouple import config

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='db_name'),
            'USER': config('DB_USER', default='db_user'),
            'PASSWORD': config('DB_PASSWORD', default='db_password'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432', cast=int), #Cast to int
        }
    }
```

## Environment Variables
Set up a `.env` file with the required configurations:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Testing
Run the test suite to ensure everything works correctly:
```bash
python manage.py test
```

## Deployment
For production deployment, use **Gunicorn and Nginx** or deploy via **Docker**:
```bash
docker build -t diversedatahub-backend .
docker run -p 8000:8000 diversedatahub-backend
```
Alternatively, deploy on **Heroku, AWS, or DigitalOcean**.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write clear and concise commit messages.
4. Open a Pull Request (PR).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


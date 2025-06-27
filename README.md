# Recipe API

A robust Django REST API for managing recipes, ingredients, and user authentication. Built with Django REST Framework following **Test-Driven Development (TDD)** architecture and designed for scalability with Docker containerization. **Production-ready with Nginx reverse proxy and uWSGI**.

## 🚀 Features

- **User Authentication**: Token-based authentication
- **Recipe Management**: Create, read, update, and delete recipes
- **Ingredient Management**: Manage recipe ingredients with quantities
- **Tag System**: Organize recipes with custom tags
- **Image Upload**: Support for recipe images
- **RESTful API**: Clean, RESTful API design with automatic documentation
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **PostgreSQL**: Production-ready database backend
- **API Documentation**: Auto-generated API docs with drf-spectacular
- **TDD Architecture**: Built following Test-Driven Development principles
- **Production Ready**: Nginx reverse proxy with uWSGI for high performance

## 🛠️ Tech Stack

- **Backend**: Django 3.2, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Token Authentication
- **Documentation**: drf-spectacular
- **Containerization**: Docker, Docker Compose
- **Image Processing**: Pillow
- **Server**: uWSGI
- **Testing**: Django Test Framework (TDD approach)
- **Production Server**: Nginx (reverse proxy)
- **Process Manager**: uWSGI

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- PostgreSQL (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd recipe-api
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/schema/swagger-ui/

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd recipe-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements.dev.txt
   ```

4. **Set up environment variables**
   ```bash
   export DEBUG=1
   export DB_HOST=localhost
   export DB_NAME=recipe_db
   export DB_USER=your_username
   export DB_PASS=your_password
   ```

5. **Run migrations**
   ```bash
   cd app
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## 🚀 Production Deployment

### Production Architecture

The production setup uses a **three-tier architecture**:
- **Nginx**: Reverse proxy and static file serving
- **uWSGI**: Application server running Django
- **PostgreSQL**: Database backend

### Production Environment Variables

Create a `.env` file for production:

```bash
# Database Configuration
DB_NAME=recipe_production
DB_USER=recipe_user
DB_PASS=secure_password

# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Optional: SSL Configuration
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

### Deploy to Production

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your production values
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.deploy.yml up -d --build
   ```

3. **Collect static files**
   ```bash
   docker-compose -f docker-compose.deploy.yml exec app python manage.py collectstatic --noinput
   ```

4. **Run migrations**
   ```bash
   docker-compose -f docker-compose.deploy.yml exec app python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose -f docker-compose.deploy.yml exec app python manage.py createsuperuser
   ```

### Production URLs

- **API**: http://your-domain.com/api/
- **Admin**: http://your-domain.com/admin/
- **API Documentation**: http://your-domain.com/api/schema/swagger-ui/

## 🌐 Nginx Configuration

### Production Nginx Setup

The production environment uses Nginx as a reverse proxy with the following configuration:

```nginx
server {
    listen 8000;
    
    location /static {
        alias /vol/static/;
    }

    location / {
        uwsgi_pass         app:9000;
        include            /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }
}
```

### Nginx Features

- **Reverse Proxy**: Routes requests to uWSGI application server
- **Static File Serving**: Serves Django static files directly
- **Load Balancing**: Ready for horizontal scaling
- **Security**: Unprivileged nginx user for enhanced security
- **File Upload Support**: 10MB max body size for image uploads

### SSL/HTTPS Setup (Optional)

To enable HTTPS, modify the Nginx configuration:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location /static {
        alias /vol/static/;
    }

    location / {
        uwsgi_pass         app:9000;
        include            /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## 📚 API Endpoints

### Authentication
- `POST /api/users/create/` - Create a new user
- `POST /api/users/token/` - Get authentication token
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update current user profile

### Recipes
- `GET /api/recipes/` - List all recipes
- `POST /api/recipes/` - Create a new recipe
- `GET /api/recipes/{id}/` - Get recipe details
- `PUT /api/recipes/{id}/` - Update recipe
- `DELETE /api/recipes/{id}/` - Delete recipe

### Tags
- `GET /api/tags/` - List all tags
- `POST /api/tags/` - Create a new tag
- `GET /api/tags/{id}/` - Get tag details
- `PUT /api/tags/{id}/` - Update tag
- `DELETE /api/tags/{id}/` - Delete tag

### Ingredients
- `GET /api/ingredients/` - List all ingredients
- `POST /api/ingredients/` - Create a new ingredient
- `GET /api/ingredients/{id}/` - Get ingredient details
- `PUT /api/ingredients/{id}/` - Update ingredient
- `DELETE /api/ingredients/{id}/` - Delete ingredient

## 🔐 Authentication

The API uses **Token Authentication**. To access protected endpoints:

1. Create a user account: `POST /api/users/create/`
2. Get an authentication token: `POST /api/users/token/`
3. Include the token in your requests:
   ```
   Authorization: Token <your_token>
   ```

### Example Authentication Flow

```bash
# Create a user
curl -X POST http://localhost:8000/api/users/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "testpass123", "name": "Test User"}'

# Get authentication token
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "testpass123"}'

# Use the token to access protected endpoints
curl -X GET http://localhost:8000/api/recipes/ \
  -H "Authorization: Token <your_token>"
```

## 📝 Example Usage

### Creating a Recipe

```bash
curl -X POST http://localhost:8000/api/recipes/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Spaghetti Carbonara",
    "time_minutes": 30,
    "price": 15.00,
    "description": "Classic Italian pasta dish",
    "link": "https://example.com/carbonara",
    "tags": [{"name": "Italian"}, {"name": "Pasta"}],
    "ingredients": [
      {"name": "Spaghetti", "amount": 500, "unit": "g"},
      {"name": "Eggs", "amount": 4, "unit": "pieces"},
      {"name": "Parmesan", "amount": 100, "unit": "g"}
    ]
  }'
```

### Getting Recipes with Filters

```bash
# Get recipes by tag
curl -X GET "http://localhost:8000/api/recipes/?tags=Italian" \
  -H "Authorization: Token <your_token>"

# Get recipes by ingredient
curl -X GET "http://localhost:8000/api/recipes/?ingredients=chicken" \
  -H "Authorization: Token <your_token>"
```

## 🧪 Testing (TDD Architecture)

This project follows **Test-Driven Development (TDD)** principles. All features are developed with comprehensive test coverage.

### Running Tests

```bash
# Run all tests with Docker
docker-compose exec app python manage.py test

# Run tests locally
cd app
python manage.py test

# Run specific app tests
python manage.py test recipe
python manage.py test users

# Run tests with coverage
python manage.py test --verbosity=2
```

### TDD Workflow

1. **Write a failing test** - Define the expected behavior
2. **Write minimal code** - Make the test pass
3. **Refactor** - Improve code quality while keeping tests green
4. **Repeat** - Continue the cycle for new features

### Test Structure

```
app/
├── recipe/
│   └── tests/
│       ├── test_models.py
│       ├── test_views.py
│       └── test_serializers.py
└── users/
    └── tests/
        ├── test_models.py
        ├── test_views.py
        └── test_serializers.py
```

## 🐳 Docker Commands

### Development
```bash
# Start development environment
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build --force-recreate
```

### Production
```bash
# Start production environment
docker-compose -f docker-compose.deploy.yml up --build

# Run in background
docker-compose -f docker-compose.deploy.yml up -d

# View production logs
docker-compose -f docker-compose.deploy.yml logs -f

# Stop production services
docker-compose -f docker-compose.deploy.yml down

# Restart specific service
docker-compose -f docker-compose.deploy.yml restart app
```

### Production Maintenance

```bash
# Update application
docker-compose -f docker-compose.deploy.yml pull
docker-compose -f docker-compose.deploy.yml up -d --build

# Backup database
docker-compose -f docker-compose.deploy.yml exec db pg_dump -U $DB_USER $DB_NAME > backup.sql

# Monitor resources
docker-compose -f docker-compose.deploy.yml ps
docker stats
```

## 📁 Project Structure

```
recipe-api/
├── app/                    # Django application
│   ├── core/              # Core Django settings
│   ├── recipe/            # Recipe app (TDD implemented)
│   │   └── tests/         # Recipe tests
│   ├── users/             # User management app (TDD implemented)
│   │   └── tests/         # User tests
│   └── manage.py          # Django management script
├── proxy/                 # Nginx configuration
│   ├── Dockerfile         # Nginx Docker image
│   ├── default.conf.tpl   # Nginx configuration template
│   ├── uwsgi_params       # uWSGI parameters
│   └── run.sh            # Nginx startup script
├── scripts/               # Docker scripts
├── docker-compose.yml     # Development Docker setup
├── docker-compose.deploy.yml  # Production Docker setup
├── Dockerfile             # Django app Docker image
├── requirements.txt       # Production dependencies
├── requirements.dev.txt   # Development dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

#### Development
- `DEBUG`: Enable/disable debug mode
- `DB_HOST`: Database host
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASS`: Database password

#### Production
- `DB_NAME`: Production database name
- `DB_USER`: Production database user
- `DB_PASS`: Production database password
- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database

The application uses PostgreSQL as the primary database. For development, you can use SQLite by modifying the database settings in `app/core/settings.py`.

### Nginx Configuration

The Nginx configuration is templated and automatically generated at runtime using environment variables:
- `LISTEN_PORT`: Port Nginx listens on (default: 8000)
- `APP_HOST`: Django app hostname (default: app)
- `APP_PORT`: Django app port (default: 9000)

## 🤝 Contributing

This project follows TDD principles. When contributing:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. **Write tests first** - Follow TDD approach
4. Implement the feature to make tests pass
5. Ensure all tests are green
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### TDD Contribution Guidelines

- Always write tests before implementing features
- Ensure test coverage for new functionality
- Follow the Red-Green-Refactor cycle
- Write meaningful test names that describe the expected behavior

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Omar Muhammed** - [omarmhd.swe@gmail.com](mailto:omarmhd.swe@gmail.com)

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:8000/api/schema/swagger-ui/)
2. Review the logs: `docker-compose logs -f`
3. Run tests to identify issues: `python manage.py test`
4. Check Nginx logs: `docker-compose -f docker-compose.deploy.yml logs proxy`
5. Open an issue on GitHub

## 🔍 Troubleshooting

### Common Issues

**Nginx not serving static files:**
```bash
docker-compose -f docker-compose.deploy.yml exec app python manage.py collectstatic --noinput
```

**Database connection issues:**
```bash
docker-compose -f docker-compose.deploy.yml exec app python manage.py wait_for_db
```

**Permission issues:**
```bash
docker-compose -f docker-compose.deploy.yml down
docker-compose -f docker-compose.deploy.yml up -d --force-recreate
```


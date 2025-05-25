# Django Template

This is a boilerplate Django project template designed to help you quickly start a new project with a preconfigured structure, useful utilities, and common Django settings. It includes commonly used settings like authentication via email, file upload handling, and base models to simplify the development process.

## Features

- **Custom Authentication Backend**: Allows authentication via email instead of username.
- **Base Model**: Provides common fields like `is_active`, `created_at`, and `updated_at` for all models.
- **Custom File Upload Paths**: Dynamic file storage paths based on a timestamp.
- **Flexible Settings**: Pre-configured settings like `ALLOWED_HOSTS`, `DEBUG`, `DATABASES`, etc., that can be easily overridden via environment variables.
- **Utilities**: Includes utility functions like `fancy_message` for custom messages, `string_to_context` for converting strings with template variables, etc.
- **Decorator Helpers**: Includes decorators like `unauthenticated_user` and `allowed_users` to manage user access based on authentication and group membership.

## Requirements

- Python 3.8 or later
- Django 4.2 or later
- PostgreSQL (or MySQL/SQLite, configurable in `settings.py`)
- Redis (optional, for caching and Celery setup)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/varlamzhordania/django-template.git
cd django-template
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the `example.env` to `development.env` and set the required environment variables. This file contains sensitive keys like your `SECRET_KEY`, database credentials, and other environment-specific settings.

```bash
cp example.env development.env
```

Edit the `.env` file with your specific settings, for example:

```ini
# Django Secret Key
DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,*

# Stripe Keys
STRIPE_SECRET_KEY=sk_***
STRIPE_PUBLISHABLE_KEY=pk_***
STRIPE_WEBHOOK_KEY=whsec_***

# Base Domains
SERVER_DOMAIN=<server_domain>
FRONTEND_DOMAIN=<frontend_domain>

# Database Configuration
DB_ENGINE=#postgresql / mysql
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email Configuration
EMAIL_HOST=<your_email_host>
EMAIL_PORT=<your_email_port>
EMAIL_USE_TLS=False
EMAIL_HOST_USER=<your_email_host_user>
EMAIL_HOST_PASSWORD=<your_email_host_password>

# Redis Configuration
REDIS_HOST=redis://redis:6379/1

# RabbitMQ
RABBITMQ_HOST=
RABBITMQ_PORT=5672
RABBITMQ_USER=
RABBITMQ_PASSWORD=
RABBITMQ_QUEUE_NAME=
```

Make sure to change the database configurations and any other settings according to your environment.

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser

Create a superuser for the admin interface:

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

Start the development server:

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Key Features and Configuration

### Authentication via Email

This template uses a custom authentication backend (`EmailBackend`) that allows users to log in with their email address rather than a username. 

To use this, ensure that your user model has an `email` field and that it's set as unique. You can customize the authentication flow if needed by modifying `account/backends.py`.

### Custom File Upload Paths

The `UploadPath` class allows you to specify dynamic file upload paths based on the folder and sub-path. It generates file paths based on a timestamp to prevent overwriting files.

Example:

```python
image = models.ImageField(upload_to=UploadPath('images', 'profile_pics'))
```

### Base Model

The `BaseModel` includes common fields like `is_active`, `created_at`, and `updated_at`. This model can be inherited by any other model in your project.

Example:

```python
class Product(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

### Utility Functions

- **`fancy_message`**: Add custom messages with different levels (`info`, `error`, `success`) to requests.
- **`string_to_context`**: Convert strings with template variables like `{{ variable_name }}` into a dictionary for use in templates.

### Decorators

- **`unauthenticated_user`**: Redirect authenticated users to a specified page (e.g., dashboard) and only allow unauthenticated users to access certain views.
  
  Example usage:
  ```python
  @unauthenticated_user
  def login_view(request):
      return render(request, 'login.html')
  ```

- **`allowed_users`**: Only allow users who belong to specific groups to access a view.

  Example usage:
  ```python
  @allowed_users(allowed_groups=['admin'])
  def admin_dashboard(request):
      return render(request, 'admin/dashboard.html')
  ```

## Deployment

## License
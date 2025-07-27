# Odoo 17 Project

## Overview
This is an Odoo 17 project designed for module development using the Odoo server framework. The project is set up with Docker for easy development and deployment.

## Features
- Odoo 17 Community Edition
- Docker-based development environment
- Custom addons directory for module development
- Example environment configuration
- Pre-configured docker-compose setup

## Prerequisites
- Docker Engine 20.10.0 or later
- Docker Compose 1.29.0 or later
- Git (for version control)

## Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd odoo17
```

### 2. Set Up Environment
Copy the example environment file and update it with your configuration:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

### 3. Start the Services
```bash
docker-compose up -d
```

### 4. Access Odoo
Open your browser and navigate to:
```
http://localhost:8069
```

## Project Structure
```
odoo17/
├── addons/          # Custom addons directory
├── etc/             # Configuration files
├── .env.example     # Example environment variables
├── docker-compose.yaml  # Docker Compose configuration
└── Makefile         # Common commands
```

## Development

### Adding New Modules
Place your custom Odoo modules in the `addons/` directory. They will be automatically discovered by Odoo.

### Useful Commands
- Start services: `docker-compose up -d`
- Stop services: `docker-compose down`
- View logs: `docker-compose logs -f`
- Access database: `docker-compose exec db psql -U odoo`

## Configuration
Edit the `docker-compose.yaml` file to customize your Odoo instance settings, such as:
- Database credentials
- Port mappings
- Volume mounts
- Environment variables

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For support, please open an issue in the repository or contact the maintainers.
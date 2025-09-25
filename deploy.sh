#!/bin/bash

# Deployment script for Digital Ocean droplet
set -e

echo "🚀 Starting deployment..."

# Variables (update these with your values)
APP_NAME="floodcontrol"
APP_DIR="/var/www/$APP_NAME"
REPO_URL="https://github.com/kpsuan/floodcontrol.git"
PYTHON_VERSION="python3.12"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib nginx git curl \
    build-essential libpq-dev

# Create application directory
print_status "Creating application directory..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone or update repository
if [ -d "$APP_DIR/.git" ]; then
    print_status "Updating existing repository..."
    cd $APP_DIR
    git pull origin main
else
    print_status "Cloning repository..."
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# Navigate to Django project
cd $APP_DIR/floodcontrol_project2

# Create virtual environment
print_status "Creating virtual environment..."
$PYTHON_VERSION -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r ../requirements-prod.txt

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput --settings=floodcontrol_project2.production_settings

# Run migrations
print_status "Running database migrations..."
python manage.py migrate --settings=floodcontrol_project2.production_settings

print_status "✅ Application setup complete!"
print_warning "Next steps:"
print_warning "1. Configure PostgreSQL database"
print_warning "2. Set up environment variables"
print_warning "3. Configure Nginx"
print_warning "4. Set up Gunicorn service"
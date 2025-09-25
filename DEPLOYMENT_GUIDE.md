# 🚀 Digital Ocean Deployment Guide

## Prerequisites
- Digital Ocean account
- Domain name (optional but recommended)
- Basic Linux command line knowledge

## Step 1: Create Digital Ocean Droplet

1. **Create a new droplet:**
   - Choose Ubuntu 22.04 LTS
   - Select $12/month droplet (2GB RAM, 1 vCPU) or higher
   - Choose a datacenter region close to your users
   - Add SSH key or use password authentication
   - Name your droplet (e.g., "floodcontrol-api")

2. **Connect to your droplet:**
   ```bash
   ssh root@your-droplet-ip
   ```

## Step 2: Initial Server Setup

```bash
# Update system
apt update && apt upgrade -y

# Create a new user (recommended for security)
adduser deploy
usermod -aG sudo deploy
su - deploy

# Generate SSH key (optional)
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

## Step 3: Install Required Software

```bash
# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib nginx git curl \
    build-essential libpq-dev certbot python3-certbot-nginx

# Install Node.js (if needed for frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## Step 4: Setup PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE floodcontrol_db;
CREATE USER floodcontrol_user WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE floodcontrol_db TO floodcontrol_user;
ALTER USER floodcontrol_user CREATEDB;
\q
```

## Step 5: Deploy Your Application

```bash
# Clone your repository
sudo mkdir -p /var/www
sudo chown deploy:deploy /var/www
cd /var/www
git clone https://github.com/kpsuan/floodcontrol.git
cd floodcontrol/floodcontrol_project2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r ../requirements-prod.txt

# Create environment file
cp ../.env.example ../.env
nano ../.env  # Edit with your actual values

# Collect static files and run migrations
python manage.py collectstatic --noinput --settings=floodcontrol_project2.production_settings
python manage.py migrate --settings=floodcontrol_project2.production_settings

# Create superuser
python manage.py createsuperuser --settings=floodcontrol_project2.production_settings
```

## Step 6: Configure Gunicorn

```bash
# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 --settings=floodcontrol_project2.production_settings floodcontrol_project2.wsgi:application

# If it works, stop it with Ctrl+C and setup as service
sudo cp ../gunicorn.socket /etc/systemd/system/
sudo cp ../gunicorn.service /etc/systemd/system/

# Create gunicorn directory
sudo mkdir -p /run/gunicorn
sudo chown www-data:www-data /run/gunicorn

# Change ownership of application files
sudo chown -R www-data:www-data /var/www/floodcontrol

# Start and enable services
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

## Step 7: Configure Nginx

```bash
# Copy nginx configuration
sudo cp ../nginx.conf /etc/nginx/sites-available/floodcontrol

# Edit the configuration file
sudo nano /etc/nginx/sites-available/floodcontrol
# Replace 'your-domain.com' and 'your-droplet-ip' with your actual values

# Enable the site
sudo ln -s /etc/nginx/sites-available/floodcontrol /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## Step 8: Setup SSL (Optional but Recommended)

```bash
# Install SSL certificate using Let's Encrypt
sudo certbot --nginx -d your-domain.com

# Auto-renewal (should be automatic)
sudo systemctl status certbot.timer
```

## Step 9: Configure Firewall

```bash
# Setup UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

## Step 10: Test Your Deployment

Visit your domain or IP address in a browser:
- `http://your-domain.com/` - Main web interface
- `http://your-domain.com/api/health/` - API health check
- `http://your-domain.com/api/floodcontrol/` - API endpoint

## Useful Commands for Maintenance

```bash
# Check application logs
sudo journalctl -u gunicorn.service -f

# Restart services
sudo systemctl restart gunicorn.service
sudo systemctl restart nginx

# Update application
cd /var/www/floodcontrol
git pull origin main
source floodcontrol_project2/venv/bin/activate
pip install -r requirements-prod.txt
python floodcontrol_project2/manage.py migrate --settings=floodcontrol_project2.production_settings
python floodcontrol_project2/manage.py collectstatic --noinput --settings=floodcontrol_project2.production_settings
sudo systemctl restart gunicorn.service
```

## Troubleshooting

1. **502 Bad Gateway Error:**
   - Check gunicorn service: `sudo systemctl status gunicorn.service`
   - Check socket file exists: `ls -la /run/gunicorn/`

2. **Static files not loading:**
   - Run: `python manage.py collectstatic --settings=floodcontrol_project2.production_settings`
   - Check nginx configuration

3. **Database connection errors:**
   - Check PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify database credentials in `.env` file

4. **Permission errors:**
   - Ensure www-data owns the application: `sudo chown -R www-data:www-data /var/www/floodcontrol`

## Security Checklist

- [ ] Use strong passwords for database and Django secret key
- [ ] Enable firewall (UFW)
- [ ] Install SSL certificate
- [ ] Regular backups of database
- [ ] Keep system updated: `sudo apt update && sudo apt upgrade`
- [ ] Monitor logs regularly

## Backup Strategy

```bash
# Database backup
pg_dump floodcontrol_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/floodcontrol
```

Your Django REST API is now deployed and ready for production use! 🎉
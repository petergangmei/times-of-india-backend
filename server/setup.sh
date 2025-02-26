#!/usr/bin/env bash

PROJECT_MAIN_DIR_NAME="toi"

sudo apt-get update
sudo apt-get upgrade -y

# Install Nginx
sudo apt install -y nginx

# Install Python3 pip
sudo apt install -y python3-pip

# Install Virtualenv
# sudo apt install -y virtualenv
sudo apt-get install python3-venv -y

# Change ownership and permissions
sudo chown -R $USER:$USER "/home/ubuntu/$PROJECT_MAIN_DIR_NAME"
sudo chmod -R 755 "/home/ubuntu/$PROJECT_MAIN_DIR_NAME"

echo "Copying gunicorn.conf file..."
sudo cp "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/server/gunicorn.service" "/etc/systemd/system/$PROJECT_MAIN_DIR_NAME.service"

sudo systemctl daemon-reload
sudo systemctl start $PROJECT_MAIN_DIR_NAME
sudo systemctl enable $PROJECT_MAIN_DIR_NAME

sudo cp "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/server/nginx.conf" "/etc/nginx/sites-available/$PROJECT_MAIN_DIR_NAME.conf"
sudo ln -s "/etc/nginx/sites-available/$PROJECT_MAIN_DIR_NAME.conf" "/etc/nginx/sites-enabled/"

sudo nginx -t
sudo systemctl restart nginx
sudo systemctl reload nginx

#create virtual environment
echo "Creating virtual environment..."
python3 -m venv "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/venv"

# Change ownership and permissions for the virtual environment
sudo chown -R $USER:$USER "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/venv"
sudo chmod -R 755 "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/venv"

# Install requirements
echo "Installing requirements..."
source "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/venv/bin/activate"
pip install psycopg2-binary gunicorn gevent
pip install -r "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/requirements.txt"

# Migrate
echo "Migrating..."
python "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/manage.py" migrate

# Collect static
# echo "Collecting static files..."
# python "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/manage.py" collectstatic

# Restart gunicorn
echo "Restarting gunicorn..."
sudo systemctl daemon-reload
sudo systemctl restart $PROJECT_MAIN_DIR_NAME.service
sudo systemctl reload nginx

echo "Done!"

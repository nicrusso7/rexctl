#!/bin/bash
# setup uwsgi service
mkdir -p /var/www/portal
chown -R "$USER" /var/www/portal
touch /tmp/portal.sock
chown www-data /tmp/portal.sock
rm -f /etc/nginx/sites-available/default
rm -f /etc/nginx/sites-enabled/default
cp "$1"/scripts/portal /etc/nginx/sites-available/portal
ln -sfn /etc/nginx/sites-available/portal /etc/nginx/sites-enabled/portal
cp "$1"/scripts/uwsgi /etc/uwsgi/apps-available/portal.ini
ln -sfn /etc/uwsgi/apps-available/portal.ini /etc/uwsgi/apps-enabled/portal.ini
cp "$1"/server.py /var/www/portal
# start all services
service nginx restart
service uwsgi restart
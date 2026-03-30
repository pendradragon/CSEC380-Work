#!/bin/bash

service apache2 start

# Wait for MySQL container
sleep 10

# Configure qdPM database connection automatically
sed -i "s/localhost/db/" /var/www/html/qdpm/config/databases.yml

# Keep container running
tail -f /dev/null

FROM python:3.11-slim

WORKDIR /app

# Install Apache and curl for healthcheck
RUN apt-get update && \
    apt-get install -y apache2 curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY docs/requirements.txt .
RUN pip install -r requirements.txt

# Copy documentation source
COPY docs/ docs/

# Build the book
RUN jupyter-book build docs/

# Configure Apache
RUN echo "Listen 8040" > /etc/apache2/ports.conf && \
    echo '<VirtualHost *:8040>\n\
    ServerAdmin webmaster@localhost\n\
    DocumentRoot /app/docs/_build/html\n\
    <Directory /app/docs/_build/html>\n\
        Options Indexes FollowSymLinks MultiViews\n\
        AllowOverride None\n\
        Order allow,deny\n\
        allow from all\n\
        Require all granted\n\
    </Directory>\n\
    ErrorLog ${APACHE_LOG_DIR}/error.log\n\
    CustomLog ${APACHE_LOG_DIR}/access.log combined\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Set permissions
RUN chown -R www-data:www-data /app/docs/_build/html && \
    chmod -R 755 /app/docs/_build/html

# Enable the site and required modules
RUN a2ensite 000-default.conf && \
    a2enmod rewrite

# Set Apache environment variables
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2/apache2.pid

# Create required directories
RUN mkdir -p /var/run/apache2 /var/lock/apache2 && \
    chown -R www-data:www-data /var/run/apache2 /var/lock/apache2

# Start Apache in foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]

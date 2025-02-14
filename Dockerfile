FROM python:3.11-slim

WORKDIR /app

# Install Apache
RUN apt-get update && \
    apt-get install -y apache2 && \
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
        Options Indexes FollowSymLinks\n\
        AllowOverride All\n\
        Require all granted\n\
    </Directory>\n\
    ErrorLog ${APACHE_LOG_DIR}/error.log\n\
    CustomLog ${APACHE_LOG_DIR}/access.log combined\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Enable the site
RUN a2ensite 000-default.conf

# Start Apache in foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]

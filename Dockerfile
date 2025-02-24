FROM python:3.10-slim

# The container will always run in /docs
WORKDIR /docs

# We won't COPY here, because we rely on the volume mount for local dev.

# Install dependencies
RUN pip install --no-cache-dir -r docs/requirements.txt

EXPOSE 8040

# Start a live server that rebuilds on changes
CMD ["sphinx-autobuild", ".", "_build/html", "--port", "8040", "--host", "0.0.0.0"]

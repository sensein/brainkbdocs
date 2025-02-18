FROM python:3.10-slim

# Install dependencies
RUN pip install --no-cache-dir \
    jupyter-book \
    sphinx-autobuild \
    sphinxcontrib-mermaid

# The container will always run in /docs
WORKDIR /docs

# We won't COPY here, because we rely on the volume mount for local dev.

EXPOSE 8040

# Start a live server that rebuilds on changes
CMD ["sphinx-autobuild", ".", "_build/html", "--port", "8040", "--host", "0.0.0.0"]

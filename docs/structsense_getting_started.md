# Getting Started
<!-- # Installation-->
## Installation
You can install the latest version of StructSense directly from PyPI using pip:
```bash
pip install structsense
```
Alternatively, you can install the latest version of StructSense from the source code on GitHub:

```bash
git clone https://github.com/sensein/structsense.git
cd structsense
pip install -e .
```
### Python Version
StructSense supports **Python >=3.10,<3.13**.


<!-- # Requirements -->
## Requirements
### PDF Extraction with Grobid

StructSense supports PDF extraction using **[Grobid](https://grobid.readthedocs.io/en/latest/Introduction/)** (default) or an external API service.

#### Default: Grobid
By default, StructSense uses Grobid for PDF extraction. You can install and run Grobid either with Docker or in a non-Docker setup.  
We recommend using Docker for easier setup and dependency management.

##### Run Grobid with Docker
```bash
docker pull lfoppiano/grobid:0.8.0
docker run --init -p 8070:8070 -e JAVA_OPTS="-XX:+UseZGC" lfoppiano/grobid:0.8.0
```
> **Note:** The `JAVA_OPTS="-XX:+UseZGC"` flag helps prevent a macOS-specific error.

#### Alternative: Remote Service (e.g., Remote Grobid)
If you prefer to use a remote service, set the environment variable as follows:
```bash
export GROBID_SERVER_URL_OR_EXTERNAL_SERVICE=http://your-remote-grobid:PORT
```

### External PDF Extraction API
If using a non‑Grobid API:
```bash
export GROBID_SERVER_URL_OR_EXTERNAL_SERVICE=https://api.SOMEAPIENDPOINT.com/api/extract
export EXTERNAL_PDF_EXTRACTION_SERVICE=True
```
> The external API is assumed public (no auth) for now.

<!--Running -->

## Running

### Using OpenRouter
```bash
structsense-cli extract \
  --source somefile.pdf \
  --api_key <YOUR_API_KEY> \
  --config someconfig.yaml \
  --env_file .env \
  --save_file result.json  # optional
```

### Using Ollama (Local)
```bash
structsense-cli extract \
  --source somefile.pdf \
  --config someconfig.yaml \
  --env_file .env_file \
  --save_file result.json  # optional
```

### Chunking
Disabled by default. Enable with:
```bash
--chunking True
```

<!-- Docker -->
## Using Docker Compose

The `docker/` directory contains **Docker Compose** files for running the following components:

- **Grobid** – for PDF extraction
- **Ollama** – In our setup, Ollama is used for embedding generation. However, it can also serve as a substitute for OpenRouter when using open-source models such as Llama for agents. OpenRouter, on the other hand, provides access to various proprietary models like GPT.
- **Weaviate** – In our StructSense architecture, Weaviate acts as the vector database responsible for storing the ontology, effectively serving as the Ontology database.

These Compose files allow you to quickly stand up a complete local **StructSense** stack.

If you prefer not to install dependencies system-wide, you can use the provided Docker Compose setup to run everything in **container mode**.  
This makes it easy to isolate services and manage your environment with minimal setup.

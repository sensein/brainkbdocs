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

## Optional Services
- **Grobid** (PDF parsing)
- **Weaviate** (vector database for knowledge/ontology)
- **Ollama** (local LLM/embedding provider)
- **MLflow / Weights & Biases** (experiment tracking)

<!-- # Requirements -->
## Requirements
### PDF Extraction (Grobid)

By default StructSense uses a **local Grobid** service. If Grobid is running locally, no extra setup is needed.

#### Run Grobid with Docker
```bash
docker pull lfoppiano/grobid:0.8.0
docker run --init -p 8070:8070 -e JAVA_OPTS="-XX:+UseZGC" lfoppiano/grobid:0.8.0
```
`JAVA_OPTS="-XX:+UseZGC"` helps avoid a macOS-specific error.

#### Remote Grobid
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
## Docker

The `docker/` directory contains compose files (individual and merged) to run:
- **Grobid**
- **Ollama**
- **Weaviate** (vector DB)

Use these to stand up a local end‑to‑end stack for StructSense.

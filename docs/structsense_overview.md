# 🧩 StructSense

**StructSense** is a multi‑agent system that extracts **structured information** from unstructured sources like PDFs and scientific text.  
It orchestrates specialized agents to collaborate, align to schemas/ontologies, and emit JSON outputs suitable for knowledge graphs and downstream analytics.

> ⚠️ This package is under active development and may change rapidly.

## Why StructSense?
- 🔍 **Structured extraction** from messy text (PDFs, docs, articles)
- 🤝 **Agent collaboration** (extract → align → judge → feedback)
- 🧠 **Domain‑agnostic** design guided by ontologies/schemas
- ⚙️ **Easy to run** via CLI, with local or remote PDF parsing backends

## Architecture
![StructSense Architecture](images/structsense_arch.png)

## Quickstart
```bash
pip install structsense

structsense-cli extract \
  --source somefile.pdf \
  --config someconfig.yaml \
  --env_file .env \
  --save_file result.json
```

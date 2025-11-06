<!-- # Known Issues & Troubleshooting-->
# Known Issues & Troubleshooting

## pip “resolution-too-deep”
**Symptom**
- During installation, `pip` backtracks across many `opentelemetry-*` packages and fails.

**Workaround**
```bash
pip install --use-deprecated=legacy-resolver structsense
```

## Python Version / No Matching Distribution
**Symptom**
```
ERROR: Could not find a version that satisfies the requirement structsense (from versions: none)
ERROR: No matching distribution found for structsense
```
Ensure Python version is **>=3.10,<3.13**.

<!-- FAQ -->
# FAQ

**Q: Do I need Weaviate to run StructSense?**  
A: No. Set `ENABLE_KG_SOURCE=false` to run without a vector DB.

**Q: Can I use local models without API keys?**  
A: Yes, via **Ollama**. Update agent configs to use the Ollama base URL and model.

**Q: Where do I find a minimal `.env`?**  
A: See **Environment Variables → Minimal** section.

<!-- # Known Issues & Troubleshooting-->
# Troubleshooting and FAQ
## Troubleshooting

### pip “resolution-too-deep”
**Symptom**
- During installation, `pip` backtracks across many `opentelemetry-*` packages and fails.

**Workaround**
```bash
pip install --use-deprecated=legacy-resolver structsense
```

### Python Version / No Matching Distribution
**Symptom**
```
ERROR: Could not find a version that satisfies the requirement structsense (from versions: none)
ERROR: No matching distribution found for structsense
```
**Workaround**\
Ensure Python version is **>=3.10,<3.13**.

<!-- FAQ -->
## FAQ

**Q: Why does the agent prompt “Would you like to view your execution traces?”**  
A: This happens when execution tracing or telemetry is enabled by default. You can disable the prompt by turning off tracing and telemetry via environment variables.

```bash
CREWAI_TRACING_ENABLED=false
CREWAI_DISABLE_TELEMETRY=true
CREWAI_DISABLE_TRACING=true
CREWAI_TELEMETRY=false
OTEL_SDK_DISABLED=true
ENABLE_CREW_MEMORY=false
```
**Q: I am seeing non-fatal agent memory errors. What should I do?**  
A: This is commonly related to agent memory being enabled without a valid OpenAI key. If you don’t need memory, disable it explicitly.

```bash
ENABLE_CREW_MEMORY=false
```

**Q: How do chunk sizes affect performance and accuracy?**  
A: Smaller chunk sizes generally improve extraction accuracy, but they also increase processing time. Larger chunks run faster but may reduce accuracy—choose based on your priority.


**Q: Can I use local models without API keys?**  
A: Yes, via **Ollama**. Update agent configs to use the Ollama base URL and model.

**Q: Where do I find a minimal `.env`?**  
A: See **Environment Variables → Minimal** section.



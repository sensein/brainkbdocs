# BrainKB Documentation

This repository contains the Jupyter Book documentation for BrainKB.

## Requirements

```
pip install -r docs/requirements.txt
```

## Running

Auto build upon changes

```
sphinx-autobuild . _build/html
```

Auto build upon changes and open browser

```
sphinx-autobuild . _build/html --open-browser
```


Build and watch the Jupyter Book on port other than 8000, i.e., the default one.

```
sphinx-autobuild . _build/html --open-browser --port 8009  
```

**Note:** 
- If the Mermaid extension does not automatically add `sphinxcontrib.mermaid` to the generated `conf.py`, you will need to manually include it in the `extensions` list to enable rendering of Mermaid diagrams.
- You need to be inside the jupyterbook directory and run the command, otherwise, replace **"."** with appropriate path.


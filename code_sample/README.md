# Public code sample

This directory contains two small, dependency-free excerpts adapted from the private Career OS backend:

- `location.py` normalizes inconsistent job-board location text without treating an unknown location as German or foreign.
- `public_fit.py` maps an internal fit assessment to the allow-listed response used by the interface. Similarity, ranking weight, and the internal seniority label stay inside the service.

The files are intentionally narrow. They show the handling of uncertain input, typed boundaries, and tests without exposing source adapters, ranking logic, profile evidence, application data, or material-generation code.

Run the sample tests from the repository root:

```bash
python -m unittest discover -s code_sample -p "test_*.py"
```

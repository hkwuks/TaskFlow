# TaskFlow evals

Run the offline suite from the repository root:

```bash
python3 evals/runner.py
```

Each skill gets one file under `evals/cases/`. Cases combine at least three positive and two negative routing prompts with artifact expectations. Fixtures are immutable sample task trees; no network, model, or third-party dependency is required. A case fails on incomplete schema, missing fixtures, unknown kinds, or unmet expectations.

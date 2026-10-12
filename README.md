# Task Manager

A small Python task-manager project used for Claude Code practice.

## Commands

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run tests:

```bash
python3 -m pytest -v
```

Lint:

```bash
python3 -m ruff check .
```

## Architecture

The project follows:

`routes -> services -> repositories`

- `routes/` handles input-facing functions
- `services/` contains business logic
- `repositories/` stores and retrieves data
- `utils/errors.py` contains project-specific errors

# CLAUDE_v1.md

## Commands
- Install dependencies with `python3 -m pip install -r requirements.txt`.
- Run tests with `python3 -m pytest -v`.
- Run lint with `python3 -m ruff check .`.
- Before finishing a task, run `python3 -m pytest -v`.

## Architecture
- Keep the project flow as `routes -> services -> repositories`.
- Put business logic in `services/`, not in route files.
- Use `services/users.py` as the main example for service-layer code.
- Follow the existing patterns in `services/tasks.py` when changing task behavior.

## Conventions
- Use type hints for new or modified functions.
- Use Google-style docstrings for new or modified functions.
- Follow `services/users.py` as the style pattern.
- Use `AppError` subclasses from `utils/errors.py` instead of raw exceptions when one fits.
- Keep existing function signatures unless the task specifically requires a change.

## Do not touch
- Do not bypass the `routes -> services -> repositories` structure.
- Do not move business logic into `routes/`.
- Do not replace errors from `utils/errors.py` with generic exceptions.
- Do not edit unrelated files just for cleanup.

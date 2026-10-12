# CLAUDE.md

## Commands
- Install dependencies with `python -m pip install -r requirements.txt`.
- Run tests with `python -m pytest -v`.
- Run lint with `python -m ruff check .`.
- Before finishing any code task, run `python -m pytest -v` and fix any failures caused by the changes.
- In this project, use the virtual environment: run tests with `.venv/bin/python3 -m pytest -q` and lint with `.venv/bin/python3 -m ruff check .` (system `python3` does not have pytest installed).

## Architecture
- Keep the project structure as `routes -> services -> repositories`.
- Routes should handle requests and responses, services should contain the main logic, and repositories should handle data access.
- Use `services/users.py` as the example to follow for service-layer code.
- Follow the existing style in `services/tasks.py` when changing or adding task functions.
- Do not call repository logic directly from a route if the project already expects that logic to go through a service.
- `routes/users.py` should only call functions in `services/users.py`, where notification preference validation and business logic happen, following the existing pattern in `services/users.py`.

## Conventions
- Use type hints for all new or modified functions.
- Use Google-style docstrings for all new or modified functions.
- Match the style in `services/users.py` when writing service functions.
- Use the `AppError` subclasses from `utils/errors.py` instead of plain built-in exceptions when a project-specific error fits.
- Keep existing function signatures unless the task specifically requires a change.
- Keep changes focused on the task instead of rewriting unrelated code.
- Add or update tests when service behavior changes.
- For refactors that do not change behavior, keep the existing tests and avoid adding unnecessary new tests.

## Do not touch
- Do not break the `routes -> services -> repositories` structure.
- Do not move service logic into route files.
- Do not replace the error handling in `utils/errors.py` with generic exceptions.
- Do not rename or remove existing public service functions unless the task asks for it.
- Do not edit unrelated files just for cleanup.
- Do not import from `repositories/users.py` in `routes/users.py` or any other route file; routes must go through `services/users.py`.
- Do not validate notification preferences (`email`, `sms`, `none`) in `routes/users.py`; validation belongs in `services/users.py`.
- Do not return HTTP responses or put route-style logic in `services/users.py`; services return data or raise `AppError` subclasses from `utils/errors.py`.
- Do not add validation or business rules to `repositories/users.py`; it only stores and retrieves user data, and the stored field must be named `notification_pref`.
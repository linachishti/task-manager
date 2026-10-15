# Endpoint Scaffold

## Goal

Use `$ARGUMENTS` as two values: the resource name and HTTP method (for example, `tags POST`).

Create or update the necessary files:

- `routes/<resource>.py` — endpoint handler
- `services/<resource>.py` — business logic
- `schemas/<resource>.py` — request and response schemas

If a required file already exists, update it instead of replacing it.

## Context

Follow `routes/tasks.py` as the canonical route pattern. Use `services/tasks.py` for service-layer conventions and `utils/errors.py` for error handling.

Check whether the project has a working HTTP framework before implementing the endpoint.

## Constraints

- Do not put business logic or validation inside route handlers.
- Routes must call service functions rather than accessing repositories directly.
- Do not modify `utils/errors.py` or unrelated files.
- Preserve existing functions and tests.
- If the project lacks HTTP infrastructure, explain what is needed and request approval before adding dependencies or a framework.

## Verification

Run `.venv/bin/python3 -m pytest -q` and `.venv/bin/python3 -m ruff check .`.

Verify that the new endpoint returns the expected HTTP status code on a successful request, such as `200 OK` for GET or `201 Created` for POST.

If a real HTTP request cannot be tested because the project has no HTTP framework, report that verification as incomplete. Do not claim that calling a Python function verifies an HTTP status code.
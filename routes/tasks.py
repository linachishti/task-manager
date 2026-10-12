"""Task route-style functions.

These functions are intentionally simple so the architecture is easy to see.
"""

from services.tasks import (
    DEFAULT_PRIORITY,
    create_task,
    filter_tasks_by_priority,
    get_task,
    update_task_priority,
)


def show_task(task_id: int) -> dict:
    """Return task information through the service layer."""
    return get_task(task_id)


def add_task(title: str, user_id: int, priority: int = DEFAULT_PRIORITY) -> dict:
    """Create a task through the service layer.

    Args:
        title: Title of the task to create.
        user_id: ID of the user who owns the task.
        priority: Priority of the task, from 1 to 5. Defaults to DEFAULT_PRIORITY.

    Returns:
        The newly created task.
    """
    return create_task(title, user_id, priority)


def update_task(task_id: int, priority: int) -> dict:
    """Update a task's priority through the service layer.

    Args:
        task_id: ID of the task to update.
        priority: New priority of the task, from 1 to 5.

    Returns:
        The updated task.
    """
    return update_task_priority(task_id, priority)


def list_tasks_by_priority(priority: int) -> list[dict]:
    """Return tasks with the given priority through the service layer.

    Equivalent to GET /tasks?priority={n}.

    Args:
        priority: Priority to filter by, from 1 to 5.

    Returns:
        The matching tasks, or an empty list if none match.
    """
    return filter_tasks_by_priority(priority)

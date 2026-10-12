"""In-memory task repository."""

DEFAULT_PRIORITY = 3

_TASKS = {
    1: {"id": 1, "title": "Finish homework", "user_id": 1, "priority": 3},
    2: {"id": 2, "title": "Study for quiz", "user_id": 1, "priority": 3},
    3: {"id": 3, "title": "Write reflection", "user_id": 2, "priority": 3},
}


def get_task_by_id(task_id: int) -> dict | None:
    """Return a task by ID, or None if it does not exist."""
    return _TASKS.get(task_id)


def create_task_record(
    title: str, user_id: int, priority: int = DEFAULT_PRIORITY
) -> dict:
    """Create and store a new task.

    The priority is stored as given. Validation belongs in the service layer.

    Args:
        title: Title of the task to create.
        user_id: ID of the user who owns the task.
        priority: Priority of the task. Defaults to DEFAULT_PRIORITY.

    Returns:
        The newly created task.
    """
    next_id = max(_TASKS, default=0) + 1
    task = {"id": next_id, "title": title, "user_id": user_id, "priority": priority}
    _TASKS[next_id] = task
    return task


def update_task_priority_record(task_id: int, priority: int) -> dict | None:
    """Update the priority of a stored task.

    The priority is stored as given. Validation belongs in the service layer.

    Args:
        task_id: ID of the task to update.
        priority: New priority of the task.

    Returns:
        The updated task, or None if the task does not exist.
    """
    task = _TASKS.get(task_id)
    if task is None:
        return None
    task["priority"] = priority
    return task


def get_all_tasks() -> list[dict]:
    """Return all stored tasks."""
    return list(_TASKS.values())


def get_tasks_by_priority(priority: int) -> list[dict]:
    """Return all stored tasks with the given priority.

    The priority is used as given. Validation belongs in the service layer.

    Args:
        priority: Priority to match.

    Returns:
        The matching tasks in ID order, or an empty list if none match.
    """
    return [task for task in _TASKS.values() if task["priority"] == priority]

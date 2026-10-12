import pytest

from routes.tasks import add_task, list_tasks_by_priority, show_task, update_task
from utils.errors import NotFoundError, ValidationError

FILTER_TASKS = {
    1: {"id": 1, "title": "Low", "user_id": 1, "priority": 1},
    2: {"id": 2, "title": "Medium A", "user_id": 1, "priority": 3},
    3: {"id": 3, "title": "Medium B", "user_id": 2, "priority": 3},
    4: {"id": 4, "title": "High", "user_id": 2, "priority": 5},
}


@pytest.fixture
def filter_tasks(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "repositories.tasks._TASKS",
        {task_id: dict(task) for task_id, task in FILTER_TASKS.items()},
    )


def test_add_task_defaults_priority_to_3() -> None:
    task = add_task("Route task", 1)
    assert task["priority"] == 3


def test_add_task_stores_priority() -> None:
    task = add_task("High priority route task", 1, 5)
    assert task["priority"] == 5
    assert show_task(task["id"])["priority"] == 5


def test_add_task_rejects_invalid_priority() -> None:
    with pytest.raises(ValidationError):
        add_task("Invalid route task", 1, 6)


def test_update_task_changes_priority() -> None:
    task = add_task("Route task to update", 1)
    updated = update_task(task["id"], 1)
    assert updated["priority"] == 1
    assert show_task(task["id"])["priority"] == 1


def test_update_task_rejects_invalid_priority() -> None:
    task = add_task("Route task with invalid update", 1)
    with pytest.raises(ValidationError):
        update_task(task["id"], 0)


def test_update_task_raises_for_missing_task() -> None:
    with pytest.raises(NotFoundError):
        update_task(999, 4)


def test_update_task_validates_priority_before_task_exists() -> None:
    with pytest.raises(ValidationError):
        update_task(999, 0)


def test_route_responses_include_priority() -> None:
    created = add_task("Response check task", 1)
    assert "priority" in created
    assert "priority" in show_task(created["id"])
    assert "priority" in update_task(created["id"], 2)


def test_list_tasks_by_priority_returns_matching_tasks(filter_tasks: None) -> None:
    tasks = list_tasks_by_priority(5)
    assert [task["id"] for task in tasks] == [4]


def test_list_tasks_by_priority_returns_empty_list_when_none_match(
    filter_tasks: None,
) -> None:
    assert list_tasks_by_priority(2) == []


def test_list_tasks_by_priority_rejects_invalid_priority(filter_tasks: None) -> None:
    with pytest.raises(ValidationError):
        list_tasks_by_priority(0)

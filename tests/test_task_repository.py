import pytest

from repositories.tasks import (
    create_task_record,
    get_task_by_id,
    get_tasks_by_priority,
    update_task_priority_record,
)

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


def test_create_task_record_defaults_priority_to_3() -> None:
    task = create_task_record("Plan week", 1)
    assert task["priority"] == 3
    assert get_task_by_id(task["id"])["priority"] == 3


def test_create_task_record_stores_priority_1() -> None:
    task = create_task_record("Low priority task", 1, priority=1)
    assert task["priority"] == 1
    assert get_task_by_id(task["id"])["priority"] == 1


def test_create_task_record_stores_priority_5() -> None:
    task = create_task_record("High priority task", 1, priority=5)
    assert task["priority"] == 5
    assert get_task_by_id(task["id"])["priority"] == 5


def test_update_task_priority_record_changes_stored_priority() -> None:
    task = create_task_record("Repository update task", 1)
    updated = update_task_priority_record(task["id"], 4)
    assert updated["priority"] == 4
    assert get_task_by_id(task["id"])["priority"] == 4


def test_update_task_priority_record_returns_none_for_missing_task() -> None:
    assert update_task_priority_record(999, 4) is None


def test_get_tasks_by_priority_returns_matching_tasks(filter_tasks: None) -> None:
    tasks = get_tasks_by_priority(3)
    assert [task["id"] for task in tasks] == [2, 3]


def test_get_tasks_by_priority_returns_empty_list_when_none_match(
    filter_tasks: None,
) -> None:
    assert get_tasks_by_priority(2) == []

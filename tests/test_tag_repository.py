import pytest

from repositories.tags import create_tag_record, get_all_tags


@pytest.fixture(autouse=True)
def empty_tags(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("repositories.tags._TAGS", {})


def test_create_tag_record_stores_tag_with_next_id() -> None:
    first = create_tag_record("urgent")
    second = create_tag_record("home")
    assert first == {"id": 1, "name": "urgent"}
    assert second == {"id": 2, "name": "home"}
    assert get_all_tags() == [first, second]


def test_get_all_tags_returns_empty_list_when_no_tags() -> None:
    assert get_all_tags() == []

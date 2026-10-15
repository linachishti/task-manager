import pytest

from repositories.tags import get_all_tags
from services.tags import create_tag
from utils.errors import ValidationError


@pytest.fixture(autouse=True)
def empty_tags(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("repositories.tags._TAGS", {})


def test_create_tag_returns_new_tag() -> None:
    tag = create_tag("urgent")
    assert tag == {"id": 1, "name": "urgent"}


def test_create_tag_strips_surrounding_whitespace() -> None:
    tag = create_tag("  urgent  ")
    assert tag["name"] == "urgent"


@pytest.mark.parametrize("name", ["", "   "])
def test_create_tag_rejects_blank_name(name: str) -> None:
    with pytest.raises(ValidationError):
        create_tag(name)


@pytest.mark.parametrize("name", [None, 123])
def test_create_tag_rejects_non_string_name(name: object) -> None:
    with pytest.raises(ValidationError):
        create_tag(name)


def test_create_tag_rejects_exact_duplicate() -> None:
    create_tag("urgent")
    with pytest.raises(ValidationError):
        create_tag("urgent")


def test_create_tag_rejects_duplicate_ignoring_case_and_whitespace() -> None:
    create_tag("Urgent")
    with pytest.raises(ValidationError):
        create_tag(" urgent ")
    assert len(get_all_tags()) == 1

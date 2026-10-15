"""In-memory tag repository."""

_TAGS: dict[int, dict] = {}


def create_tag_record(name: str) -> dict:
    """Create and store a new tag.

    The name is stored as given. Validation belongs in the service layer.

    Args:
        name: Name of the tag to create.

    Returns:
        The newly created tag.
    """
    next_id = max(_TAGS, default=0) + 1
    tag = {"id": next_id, "name": name}
    _TAGS[next_id] = tag
    return tag


def get_all_tags() -> list[dict]:
    """Return all stored tags."""
    return list(_TAGS.values())

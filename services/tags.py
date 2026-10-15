"""Tag service functions."""

from repositories.tags import create_tag_record, get_all_tags
from utils.errors import ValidationError


def create_tag(name: str) -> dict:
    """Create a new tag.

    Surrounding whitespace is removed before the tag is stored. Names are
    compared case-insensitively, so "Urgent" and " urgent " are duplicates.

    Args:
        name: Name of the tag to create.

    Returns:
        The newly created tag.

    Raises:
        ValidationError: If the name is not a string, is empty or only
            whitespace, or matches an existing tag name.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Tag name cannot be empty.")
    name = name.strip()
    if any(tag["name"].casefold() == name.casefold() for tag in get_all_tags()):
        raise ValidationError(f"Tag '{name}' already exists.")
    tag = create_tag_record(name)
    return tag

"""Tag HTTP routes."""

from fastapi import APIRouter, status

from schemas.tags import TagCreate, TagResponse
from services.tags import create_tag

router = APIRouter()


@router.post(
    "/tags", status_code=status.HTTP_201_CREATED, response_model=TagResponse
)
def add_tag(payload: TagCreate) -> dict:
    """Create a tag through the service layer.

    Args:
        payload: Request body containing the tag name.

    Returns:
        The newly created tag.
    """
    return create_tag(payload.name)

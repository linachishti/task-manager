"""Tag request and response schemas."""

from pydantic import BaseModel


class TagCreate(BaseModel):
    """Request body for creating a tag."""

    name: str


class TagResponse(BaseModel):
    """Response body for a tag."""

    id: int
    name: str

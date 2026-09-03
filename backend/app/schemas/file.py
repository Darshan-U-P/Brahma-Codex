from pydantic import BaseModel, Field


class FileCreate(BaseModel):
    """Request schema for creating a file."""

    path: str = Field(
        min_length=1,
        max_length=500,
        description="Relative path inside the project workspace.",
    )

    content: str = Field(
        default="",
        description="Initial file content.",
    )

    overwrite: bool = Field(
        default=False,
        description=(
            "Allow replacing an existing file."
        ),
    )


class FileUpdate(BaseModel):
    """Request schema for updating a file."""

    content: str = Field(
        description="New file content.",
    )


class FileResponse(BaseModel):
    """Response schema for file metadata."""

    path: str
    name: str
    type: str
    size: int | None = None


class FileContentResponse(BaseModel):
    """Response schema for file content."""

    path: str
    content: str


class FileOperationResponse(BaseModel):
    """Response schema for file operations."""

    success: bool
    message: str
    path: str
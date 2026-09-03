from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Project name",
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
        description="Project description",
    )

    project_type: str = Field(
        default="general",
        min_length=1,
        max_length=100,
        description="Type of project",
    )


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    project_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    project_type: str
    status: str
    workspace_path: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
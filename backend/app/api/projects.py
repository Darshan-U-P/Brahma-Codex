from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.workspace_service import workspace_service


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    """Create a new project and its workspace."""

    project = Project(
        name=project_data.name,
        description=project_data.description,
        project_type=project_data.project_type,
    )

    try:
        # Step 1: Create database record first
        db.add(project)
        db.commit()
        db.refresh(project)

        # Step 2: Create physical workspace
        workspace_path = workspace_service.create_workspace(
            project_name=project.name,
            project_id=project.id,
            project_type=project.project_type,
        )

        # Step 3: Save workspace path
        project.workspace_path = str(workspace_path)

        db.commit()
        db.refresh(project)

        return project

    except Exception as error:
        db.rollback()

        # If the database project was created but workspace
        # creation failed, remove the incomplete project.
        if project.id is not None:
            try:
                db.delete(project)
                db.commit()
            except Exception:
                db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project workspace: {str(error)}",
        ) from error


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    db: Session = Depends(get_db),
):
    """Get all projects."""

    projects = (
        db.query(Project)
        .order_by(Project.created_at.desc())
        .all()
    )

    return projects


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    """Get a project by ID."""

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found.",
        )

    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing project."""

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found.",
        )

    update_data = project_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


@router.delete(
    "/{project_id}",
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    """Delete a project and its workspace."""

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found.",
        )

    try:
        # Delete physical workspace first
        if project.workspace_path:
            workspace_service.delete_workspace(
                project.workspace_path
            )

        # Delete database record
        db.delete(project)
        db.commit()

        return {
            "success": True,
            "message": (
                f"Project with ID {project_id} "
                "and its workspace deleted successfully."
            ),
        }

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete project: {str(error)}",
        ) from error